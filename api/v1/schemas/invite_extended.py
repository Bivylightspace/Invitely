from typing import List, Optional
from enum import Enum
from pydantic import BaseModel, Field


class InviteCreateTemplate(BaseModel):
    title: str = Field(..., min_length=3, max_length=120)
    description: Optional[str] = Field(default=None, max_length=500)
    event_date: Optional[str] = None
    location: Optional[str] = Field(default=None, max_length=200)
    template_id: Optional[str] = None

    class Config:
        anystr_strip_whitespace = True


class InviteCreateUpload(BaseModel):
    title: str = Field(..., min_length=3, max_length=120)
    description: Optional[str] = Field(default=None, max_length=500)
    event_date: Optional[str] = None
    location: Optional[str] = Field(default=None, max_length=200)
    upload_path: Optional[str] = None

    class Config:
        anystr_strip_whitespace = True


class GuestCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=120)
    phone: str = Field(..., min_length=7, max_length=32)

    class Config:
        anystr_strip_whitespace = True


class InviteSendRequest(BaseModel):
    event_id: str
    guests: List[GuestCreate]


class RsvpStatus(str, Enum):
    attending = "attending"
    not_attending = "not_attending"


class RsvpCreate(BaseModel):
    status: RsvpStatus
    attendee_name: Optional[str] = None
