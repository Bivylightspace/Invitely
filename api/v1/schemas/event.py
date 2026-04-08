import enum
from pydantic import BaseModel
from datetime import datetime

class EventCreate(BaseModel):
    title: str
    description: str | None = None
    location: str
    event_date: datetime

class EventResponse(EventCreate):
    id: int

    class Config:
        from_attributes = True

class EventType(enum.Enum):
    PHYSICAL = "physical"
    VIRTUAL = "virtual"
    MIXED = "mixed"

# Enum for plan type
class Plan(enum.Enum):
    FREE = "free"
    PAID = "paid"