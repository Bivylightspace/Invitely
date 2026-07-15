from datetime import datetime, timezone
from typing import List
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from api.utils.config import settings
from api.utils.whatsapp import send_whatsapp_template
from api.v1.models.event import Event
from api.v1.models.guest import Guest
from api.v1.models.invite_link import InviteLink
from api.v1.models.rsvp import Rsvp, RsvpStatus
from api.v1.models.user import User
from api.v1.schemas.invite_extended import (
    GuestCreate,
    InviteCreateTemplate,
    InviteCreateUpload,
    InviteSendRequest,
    RsvpCreate,
)


async def create_event_template(
    invite_data: InviteCreateTemplate,
    owner: User,
    db: AsyncSession,
) -> Event:
    event = Event(
        title=invite_data.title,
        description=invite_data.description,
        event_date=invite_data.event_date,
        location=invite_data.location,
        upload_path=None,
        host_id=owner.id,
    )
    db.add(event)
    await db.flush()
    await db.commit()
    await db.refresh(event)
    return event


async def create_event_upload(
    invite_data: InviteCreateUpload,
    owner: User,
    db: AsyncSession,
) -> Event:
    event = Event(
        title=invite_data.title,
        description=invite_data.description,
        event_date=invite_data.event_date,
        location=invite_data.location,
        upload_path=invite_data.upload_path,
        host_id=owner.id,
    )
    db.add(event)
    await db.flush()
    await db.commit()
    await db.refresh(event)
    return event


async def _get_event_for_owner(event_id: str, owner: User, db: AsyncSession) -> Event:
    result = await db.execute(select(Event).where(Event.id == event_id, Event.host_id == owner.id))
    event = result.scalars().first()
    if not event:
        raise ValueError("Event not found or you do not have permission to access it.")
    return event


async def send_event_invites(request: InviteSendRequest, owner: User, db: AsyncSession) -> List[dict]:
    event = await _get_event_for_owner(request.event_id, owner, db)

    created_guests = []
    sent_notifications = []

    for guest_data in request.guests:
        guest = Guest(
            name=guest_data.name,
            phone=guest_data.phone,
            event_id=event.id,
        )
        db.add(guest)
        await db.flush()

        token = uuid4().hex
        invite_url = f"{settings.FRONTEND_URL.rstrip('/')}/i/{token}" if settings.FRONTEND_URL else f"/i/{token}"
        invite_link = InviteLink(
            token=token,
            url=invite_url,
            event_id=event.id,
            guest_id=guest.id,
            active=True,
        )
        db.add(invite_link)
        await db.flush()

        created_guests.append({
            "guest_id": guest.id,
            "name": guest.name,
            "phone": guest.phone,
            "invite_url": invite_link.url,
        })

        notification_result = await send_whatsapp_template(
            to=guest.phone,
            guest_name=guest.name,
            event_name=event.title,
            invite_link=invite_link.url,
        )
        sent_notifications.append({
            "guest_id": guest.id,
            "phone": guest.phone,
            "result": notification_result,
        })

    await db.commit()
    return sent_notifications


async def get_public_invite(token: str, db: AsyncSession) -> dict:
    statement = (
        select(InviteLink)
        .where(InviteLink.token == token, InviteLink.active == True)
        .options(
            selectinload(InviteLink.event),
            selectinload(InviteLink.guest),
        )
    )
    result = await db.execute(statement)
    invite_link = result.scalars().first()
    if not invite_link:
        raise ValueError("Invite link not found or inactive.")

    return {
        "token": invite_link.token,
        "url": invite_link.url,
        "event": {
            "id": invite_link.event.id,
            "title": invite_link.event.title,
            "description": invite_link.event.description,
            "event_date": invite_link.event.event_date,
            "location": invite_link.event.location,
            "upload_path": invite_link.event.upload_path,
        },
        "guest": {
            "id": invite_link.guest.id,
            "name": invite_link.guest.name,
            "phone": invite_link.guest.phone,
        },
    }


async def record_rsvp(token: str, rsvp_data: RsvpCreate, db: AsyncSession) -> dict:
    result = await db.execute(select(InviteLink).where(InviteLink.token == token, InviteLink.active == True))
    invite_link = result.scalars().first()
    if not invite_link:
        raise ValueError("Invite link not found or inactive.")

    existing_rsvp = await db.execute(select(Rsvp).where(Rsvp.invite_link_id == invite_link.id))
    if existing_rsvp.scalars().first():
        raise ValueError("RSVP has already been submitted for this invitation.")

    rsvp = Rsvp(
        guest_id=invite_link.guest_id,
        invite_link_id=invite_link.id,
        status=rsvp_data.status,
    )
    db.add(rsvp)
    await db.commit()
    await db.refresh(rsvp)

    return {
        "guest_id": invite_link.guest_id,
        "invite_link_id": invite_link.id,
        "status": rsvp.status,
        "response_at": rsvp.response_at.isoformat(),
    }
