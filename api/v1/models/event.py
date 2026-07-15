from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import DateTime, Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.v1.models.base import Base
from api.v1.schemas.event import EventType, Plan

if TYPE_CHECKING:
    from api.v1.models.user import User
    from api.v1.models.guest import Guest
    from api.v1.models.invite_link import InviteLink


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
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    location: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    upload_path: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    host_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)

    host: Mapped["User"] = relationship(back_populates="events")
    guests: Mapped[List["Guest"]] = relationship(
        back_populates="event", cascade="all, delete-orphan"
    )
    invite_links: Mapped[List["InviteLink"]] = relationship(
        back_populates="event", cascade="all, delete-orphan"
    )
