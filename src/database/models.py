from sqlalchemy import Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import (
    Mapped, mapped_column, DeclarativeBase, relationship
)
from typing import Optional
from sqlalchemy.sql.sqltypes import Date, DateTime
from typing import List


class Base(DeclarativeBase):
    pass


class Contact(Base):
    __tablename__ = "contacts"
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(150))
    phone: Mapped[int] = mapped_column(Integer)
    birth_date: Mapped[Date] = mapped_column(Date)
    additional_data: Mapped[Optional[str]]
    created_at: Mapped[DateTime] = mapped_column(DateTime)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id",
                   ondelete='CASCADE')
        )
    user: Mapped["User"] = relationship("User", back_populates="contact")


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(150), nullable=False, unique=True
        )
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    refresh_token: Mapped[str] = mapped_column(String(255), nullable=True)
    avatar: Mapped[str] = mapped_column(String(255), nullable=True)
    contact: Mapped[List["Contact"]] = relationship(
        "Contact", back_populates="user")
    confirmed: Mapped[bool] = mapped_column(Boolean, default=False)
