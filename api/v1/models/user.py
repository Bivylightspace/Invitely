from typing import List, Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from api.v1.models.base import Base
# from api.v1.models.auth_account import AuthAccount

class User(Base):
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(nullable=False)
    phone: Mapped[Optional[str]] = mapped_column(unique=True, nullable=True)
    
    # Relationship: One User can have multiple Auth methods (Email, Google, etc.)
    auth_accounts: Mapped[List["AuthAccount"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    
    # Relationship to Events (Placeholder based on your requirements)
    # events: Mapped[List["Event"]] = relationship(back_populates="owner")