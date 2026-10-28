from typing import Optional

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    name: Optional[str] = None
    username: Optional[str] = None
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: str
    name: Optional[str] = None
    username: Optional[str] = None
    email: EmailStr

    class Config:
        from_attributes = True
