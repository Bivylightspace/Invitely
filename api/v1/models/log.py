from typing import List, Optional, TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from api.v1.models.base import Base


class Log(Base):
    __tablename__ = "Logs"
    messages: Mapped[str] = mapped_column(nullable=False) 
