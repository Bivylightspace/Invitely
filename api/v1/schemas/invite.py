from typing import Optional
from pydantic import BaseModel, Field


class InviteCreate(BaseModel):
    title: str = Field(
        ..., 
        min_length=3, 
        max_length=120, 
        description="Event or invitation title."
    )
    description: Optional[str] = Field(
        default=None, 
        max_length=500, 
        description="Optional invite description or message."
    )
    event_date: Optional[str] = Field(
        default=None, 
        description="Optional event date/time string."
    )
    location: Optional[str] = Field(
        default=None,
        max_length=200,
        description="Optional event location."
    )

    class Config:
        anystr_strip_whitespace = True
