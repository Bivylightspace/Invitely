import imghdr
from uuid import uuid4

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.db.database import get_async_db
from api.utils.auth import get_current_user
from api.utils.config import settings
from api.utils.responses import success_response
from api.utils.supabase_client import get_supabase_client
from api.v1.models.user import User
from api.v1.schemas.invite_extended import (
    GuestCreate,
    InviteCreateTemplate,
    InviteCreateUpload,
    InviteSendRequest,
    RsvpCreate,
)
from api.v1.services.invite_service import (
    create_event_template,
    create_event_upload,
    get_public_invite,
    record_rsvp,
    send_event_invites,
)

invite_router = APIRouter(prefix="/invites", tags=["Invites"])
ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png", "image/webp"}
ALLOWED_IMAGE_TYPES = {"jpeg", "png", "webp"}


@invite_router.post("/upload-card", status_code=200, summary="Upload an invitation card image to Supabase")
async def upload_invite_card(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db),
):
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Unsupported file type. Only JPEG, PNG, and WebP images are allowed.",
        )

    raw_bytes = b""
    try:
        raw_bytes = await file.read()
        if not raw_bytes:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Uploaded file is empty.",
            )

        detected_type = imghdr.what(None, raw_bytes)
        if detected_type not in ALLOWED_IMAGE_TYPES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Uploaded file content is not a valid JPEG, PNG, or WebP image.",
            )

        safe_filename = f"{uuid4().hex}_{file.filename}"
        object_path = f"uploads/{safe_filename}"

        client = get_supabase_client()
        upload_response = client.storage.from_(settings.BUCKET_NAME).upload(
            object_path,
            raw_bytes,
            {
                "content-type": file.content_type,
                "upsert": "true",
            },
        )

        if upload_response.get("error"):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=(
                    "Supabase upload failed. "
                    f"{upload_response['error'].get('message', 'Unknown error')}"
                ),
            )

        signed_url_response = client.storage.from_(settings.BUCKET_NAME).create_signed_url(
            object_path,
            3600,
        )

        signed_url = (
            signed_url_response.get("signedURL")
            or signed_url_response.get("signed_url")
            or signed_url_response.get("data", {}).get("signed_url")
        )

        if not signed_url:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unable to generate a temporary signed URL for the uploaded file.",
            )

        return success_response(
            status_code=200,
            message="Card uploaded successfully.",
            data={"signed_url": signed_url, "path": object_path},
        )
    finally:
        await file.close()


@invite_router.post("/template", status_code=201, summary="Create a new template-based invite")
async def create_template_invite(
    invite_data: InviteCreateTemplate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db),
):
    try:
        event = await create_event_template(invite_data, current_user, db)
        return success_response(
            status_code=201,
            message="Template invite created successfully.",
            data={
                "id": event.id,
                "title": event.title,
                "description": event.description,
            },
        )
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@invite_router.post("/upload", status_code=201, summary="Create a new upload-based invite")
async def create_upload_invite(
    invite_data: InviteCreateUpload,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db),
):
    try:
        event = await create_event_upload(invite_data, current_user, db)
        return success_response(
            status_code=201,
            message="Upload invite created successfully.",
            data={
                "id": event.id,
                "title": event.title,
                "upload_path": event.upload_path,
            },
        )
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@invite_router.post("/send", status_code=200, summary="Send invites to guests via WhatsApp")
async def send_invites(
    request: InviteSendRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db),
):
    try:
        result = await send_event_invites(request, current_user, db)
        return success_response(
            status_code=200,
            message="Invites sent successfully.",
            data={"sent": result},
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))


@invite_router.post("/{invite_id}/rsvp", status_code=201, summary="Submit an RSVP for an invite")
async def submit_rsvp(
    invite_id: str,
    rsvp_data: RsvpCreate,
    db: AsyncSession = Depends(get_async_db),
):
    try:
        payload = await record_rsvp(invite_id, rsvp_data, db)
        return success_response(
            status_code=201,
            message="RSVP submitted successfully.",
            data=payload,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@invite_router.get("/public/{invite_id}", status_code=200, summary="Get public invite landing data")
async def get_public_invite_data(invite_id: str, db: AsyncSession = Depends(get_async_db)):
    try:
        payload = await get_public_invite(invite_id, db)
        return success_response(
            status_code=200,
            message="Public invite loaded successfully.",
            data=payload,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@invite_router.get("/{invite_id}", status_code=200, summary="Get invite landing data")
async def get_invite_data(invite_id: str, db: AsyncSession = Depends(get_async_db)):
    try:
        payload = await get_public_invite(invite_id, db)
        return success_response(
            status_code=200,
            message="Invite loaded successfully.",
            data=payload,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
