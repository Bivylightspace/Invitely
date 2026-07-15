from typing import TYPE_CHECKING, List
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.v1.models.base import Base

if TYPE_CHECKING:
    from api.v1.models.event import Event
    from api.v1.models.invite_link import InviteLink
    from api.v1.models.rsvp import Rsvp


class Guest(Base):
    __tablename__ = "guests"

    name: Mapped[str] = mapped_column(String(120), nullable=False)
    phone: Mapped[str] = mapped_column(String(32), nullable=False)
    event_id: Mapped[str] = mapped_column(ForeignKey("events.id"), nullable=False)

    event: Mapped["Event"] = relationship(back_populates="guests")
    invite_links: Mapped[List["InviteLink"]] = relationship(
        back_populates="guest", cascade="all, delete-orphan"
    )
    rsvps: Mapped[List["Rsvp"]] = relationship(
        back_populates="guest", cascade="all, delete-orphan"
    )
