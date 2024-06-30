from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel, Field, EmailStr


class ContactBase(BaseModel):
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    email: EmailStr
    phone: int = Field(gt=0)
    birth_date: date
    additional_data: Optional[str] = None
    created_at: datetime


class ContactUpdate(ContactBase):
    pass


class ContactResponse(ContactBase):
    id: int

    class Config:
        orm_mode = True


class UserModel(BaseModel):
    email: str
    password: str = Field(min_length=6, max_length=10)


class UserDb(BaseModel):
    id: int
    email: str
    avatar: str

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    user: UserDb
    detail: str = "User successfully created"


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
