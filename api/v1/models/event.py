from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from api.v1.models.base import Base
from api.v1.schemas.event import EventType, Plan
from sqlalchemy import DateTime, ForeignKey, Text, Enum

if TYPE_CHECKING:
    from api.v1.models.user import User 

class Event(Base):
    __tablename__ = "events"

    # Core fields
    title: Mapped[str] = mapped_column(Text, nullable=False)
    theme: Mapped[str] = mapped_column(Text, nullable=True)
    location: Mapped[str] = mapped_column(Text, nullable=True)

    # Event type (physical, virtual, mixed)
    event_type: Mapped[EventType] = mapped_column(
        Enum(EventType, name="event_type_enum"),
        nullable=False
    )

    # Plan type (free or paid)       
    plan: Mapped[Plan] = mapped_column(
        Enum(Plan, name="plan_enum"),         
        nullable=False,
        default=Plan.FREE
    )
    
    event_datetime: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )

    # Relationship to User
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
    user: Mapped["User"] = relationship("User", back_populates="events")