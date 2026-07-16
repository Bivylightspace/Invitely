from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .base import BaseModel


class Invitation(BaseModel):
    __tablename__ = "invitations"
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    email = Column(String, nullable=False)

    event = relationship("Event", back_populates="invitations")
