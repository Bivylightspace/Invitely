from sqlalchemy import Column, DateTime, Float, Integer, String
from sqlalchemy.orm import relationship

from .base import BaseModel


class Event(BaseModel):
    __tablename__ = "events"

    name = Column(String, nullable=False)
    datetime = Column(DateTime, nullable=False)
    longitude = Column(Float, nullable=False)
    latitude = Column(Float, nullable=False)
    guest_count = Column(Integer, nullable=True)
    attendee_type = Column(String, nullable=True)

    invitations = relationship("Invitation", back_populates="event")