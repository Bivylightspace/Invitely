from datetime import datetime, timezone
import uuid6  # Recommended for UUIDv7 support in Python
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import DateTime, func

class Base(DeclarativeBase):
    # UUIDv7 is time-sortable, making it faster for DB indexing than UUIDv4
    id: Mapped[str] = mapped_column(
        primary_key=True, 
        default=lambda: str(uuid6.uuid7()), 
        index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        onupdate=func.now(), 
        nullable=True
    )