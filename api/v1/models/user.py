from typing import TYPE_CHECKING, List, Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.v1.models.base import Base

if TYPE_CHECKING:
    from api.v1.models.auth_account import AuthAccount


class User(Base):
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(nullable=False)
    phone: Mapped[Optional[str]] = mapped_column(unique=True, nullable=True)

    # Relationship: One User can have multiple Auth methods (Email, Google, etc.)
    auth_accounts: Mapped[List["AuthAccount"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

    @property
    def email(self) -> Optional[str]:
        if self.auth_accounts:
            return self.auth_accounts[0].email
        return None

    @property
    def username(self) -> str:
        return self.name
