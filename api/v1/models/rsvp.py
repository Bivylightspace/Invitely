from datetime import datetime
from enum import Enum as PyEnum
from typing import TYPE_CHECKING
from sqlalchemy import DateTime, ForeignKey, String, Enum, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.v1.models.base import Base

if TYPE_CHECKING:
    from api.v1.models.guest import Guest
    from api.v1.models.invite_link import InviteLink


class RsvpStatus(str, PyEnum):
    attending = "attending"
    not_attending = "not_attending"


class Rsvp(Base):
    __tablename__ = "rsvps"

    guest_id: Mapped[str] = mapped_column(ForeignKey("guests.id"), nullable=False)
    invite_link_id: Mapped[str] = mapped_column(ForeignKey("invite_links.id"), nullable=False)
    status: Mapped[RsvpStatus] = mapped_column(Enum(RsvpStatus), nullable=False)
    response_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    guest: Mapped["Guest"] = relationship(back_populates="rsvps")
    invite_link: Mapped["InviteLink"] = relationship(back_populates="rsvp")
