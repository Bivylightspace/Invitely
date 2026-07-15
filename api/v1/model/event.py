from enum import StrEnum
from sqlalchemy import Column, Float, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.sql import func
import hashlib
from .base import BaseModel
from sqlalchemy.event import listens_for


class Event(BaseModel):
    __tablename__  = 'events'
    name = Column(String, nullable=False)  
    datetime = Column(DateTime, nullable=False)
    longitude = Column(Float, nullable=False)
    latitude = Column(Float, nullable=False)
    guest_count = Column(Integer, nullable=True)
    attendee_type = Column(StrEnum(Attendee_type), nullable=True)  # type: ignore
    
    invitations = relationship("Invitation", back_populates="event") # type: ignore
    