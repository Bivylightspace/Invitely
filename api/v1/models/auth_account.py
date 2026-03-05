from sqlalchemy import ForeignKey, String, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from api.v1.models.base import Base
from api.v1.models.user import User

class AuthAccount(Base):
    __tablename__ = "auth_accounts"

    # 'local', 'google', 'apple'
    provider: Mapped[str] = mapped_column(String(50), default="local")
    
    # This is the unique ID from the provider (or the email if local)
    provider_id: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=True)
    
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="auth_accounts")

    # DB Level Constraint: Ensure we have at least an email or a phone 
    # (Note: Phone is in the User table, so this logic is often handled in the Service layer,
    # but for this table, we ensure the identifier exists.)
    __table_args__ = (
        CheckConstraint(
            "(email IS NOT NULL) OR (provider != 'local')", 
            name="check_auth_method"
        ),
    )