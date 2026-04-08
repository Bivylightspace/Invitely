# routes/events.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from api.v1.schemas import EventCreate, EventResponse
from api.v1.services.event import (
    create_event_service,
    get_user_events_service,
    delete_event_service
)                                              
from utils.jwt_handler import get_current_user


event_router = APIRouter(
    prefix="/events",
    tags=["Events"]
)

@event_router.post("/", response_model=EventResponse)
def create_event(
    event: EventCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):                                   

    return create_event_service(
        db,
        event,
        current_user.id
    )


@event_router.get("/", response_model=list[EventResponse])
def get_user_events(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    return get_user_events_service(
        db,
        current_user.id
    )


@event_router.delete("/{event_id}")
def delete_event(
    event_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    return delete_event_service(
        db,
        event_id,
        current_user.id
    )