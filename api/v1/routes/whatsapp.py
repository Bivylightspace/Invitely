from fastapi import APIRouter, HTTPException
from api.v1.services.whatsapp_service import send_invite_notification

whatsapp_router = APIRouter(prefix="/whatsapp", tags=["WhatsApp"])

@whatsapp_router.post("/send-invite")
async def send_invite(to: str, guest_name: str, event_name: str, invite_link: str):
    try:
        result = await send_invite_notification(to, guest_name, event_name, invite_link)
        return {"status": "sent", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
