from typing import TYPE_CHECKING, List, Optional
from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.v1.models.base import Base

if TYPE_CHECKING:
    from api.v1.models.user import User
    from api.v1.models.guest import Guest
    from api.v1.models.invite_link import InviteLink


class Event(Base):
    __tablename__ = "events"

    title: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    event_date: Mapped[Optional[str]] = mapped_column(String(80), nullable=True)
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
