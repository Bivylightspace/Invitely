import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, UUID
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class BaseModel(Base):
    _abstract_ = True
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
