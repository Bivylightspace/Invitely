from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.sql import func
from db.base import Base
import hashlib
from sqlalchemy.event import listens_for

class Invitation(Base):
    __tablename_ = "Invitation"
    event_id = Column(Integer, ForeignKey)
    email = Column(String, nullable=False) 
    
    event = relationship("Event", back_populates="Invitations") # type: ignore