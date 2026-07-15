from sqlalchemy.orm import Session
from fastapi import HTTPException
from api.v1.models.event import Event
from api.v1.schemas.event import EventCreate


def create_event_service(db: Session, event_data: EventCreate, user_id: int):

    new_event = Event(
        title=event_data.title,
        description=event_data.description,
        location=event_data.location,
        event_date=event_data.event_date,
        owner_id=user_id
    )

    db.add(new_event)
    db.commit()
    db.refresh(new_event)

    return new_event



def get_user_events_service(db: Session, user_id: int):

    return db.query(Event).filter(
        Event.owner_id == user_id
    ).all()



def delete_event_service(db: Session, event_id: int, user_id: int):

    event = db.query(Event).filter(
        Event.id == event_id,
        Event.owner_id == user_id
    ).first()

    if not event:
        raise HTTPException(
            status_code=404,
            detail="Event not found or unauthorized"
        )

    db.delete(event)
    db.commit()

    return {"message": "Event deleted successfully"}