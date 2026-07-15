from datetime import datetime

import uuid6
from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

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