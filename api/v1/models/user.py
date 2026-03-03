from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db.base import BaseModel

class User(BaseModel):
    __tablename__ = "users"

    email = Column(String(100), unique=True, index=True)
    password = Column(String(255)) 

