from sqlalchemy import ForeignKey, String, CheckConstraint, Index, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from api.v1.schemas.user import AuthProvider
from api.v1.models.base import Base
from typing import TYPE_CHECKING 

if TYPE_CHECKING:
    from api.v1.models import User 

class AuthAccount(Base):
    __tablename__ = "auth_accounts"           

    # 'local', 'google', 'apple'    
    provider: Mapped[AuthProvider] = mapped_column(
        Enum(AuthProvider), 
        default=AuthProvider.EMAIL,
        nullable=False
    )    
    # This is the unique ID from the provider (or the email if local)
    provider_id: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=True)
    
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="auth_accounts") 

    __table_args__ = (
        Index("uix_provider_user", "provider", "user_id", unique=True),
        # Updated Constraint to match your new 'email' enum name
        CheckConstraint(
            f"(provider != '{AuthProvider.EMAIL.value}') OR (password_hash IS NOT NULL)", 
            name="check_email_auth_has_password"
        ),
    )