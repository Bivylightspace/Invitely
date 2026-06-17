from fastapi import APIRouter, HTTPException, status
from api.v1.services.whatsapp_service import send_invite_notification
from api.utils.responses import success_response, fail_response

whatsapp_router = APIRouter(prefix="/whatsapp", tags=["WhatsApp"])

@whatsapp_router.post("/send-invite")
async def send_invite(to: str, guest_name: str, event_name: str, invite_link: str):
    try:
        result = await send_invite_notification(to, guest_name, event_name, invite_link)
        return success_response(
            status_code=200,
            message="WhatsApp invite sent successfully.",
            data={"result": result}
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
