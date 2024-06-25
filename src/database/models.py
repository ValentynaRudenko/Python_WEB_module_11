from sqlalchemy import Integer, String
from sqlalchemy.orm import (
    Mapped, mapped_column, DeclarativeBase
)
from typing import Optional
# from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Date, DateTime


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
