from typing import TYPE_CHECKING, Optional
from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.v1.models.base import Base

if TYPE_CHECKING:
    from api.v1.models.event import Event
    from api.v1.models.guest import Guest
    from api.v1.models.rsvp import Rsvp


class InviteLink(Base):
    __tablename__ = "invite_links"

    token: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    event_id: Mapped[str] = mapped_column(ForeignKey("events.id"), nullable=False)
    guest_id: Mapped[str] = mapped_column(ForeignKey("guests.id"), nullable=False)
    active: Mapped[bool] = mapped_column(Boolean(), default=True, nullable=False)

    event: Mapped["Event"] = relationship(back_populates="invite_links")
    guest: Mapped["Guest"] = relationship(back_populates="invite_links")
    rsvp: Mapped[Optional["Rsvp"]] = relationship(back_populates="invite_link", uselist=False)
