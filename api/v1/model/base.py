from sqlalchemy import Column, UUID, DateTime, 
from sqlalchemy.ext.declarative import declarative_base
import uuid
from datetime import datetime

Base = declarative_base()  

class BaseModel(Base) :
    _abstract_ = True
    id = Column(UUID(as_uuid=True),primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)