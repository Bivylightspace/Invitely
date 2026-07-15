from sqlalchemy import Column, String

from .base import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    email = Column(String(100), unique=True, index=True)
    password = Column(String(255))

