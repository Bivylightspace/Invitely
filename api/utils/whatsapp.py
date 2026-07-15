import httpx

from api.utils.config import settings

BASE_WHATSAPP_URL = f"https://graph.facebook.com/v25.0/{settings.WHATSAPP_PHONE_NUMBER_ID}/messages"
HEADERS = {
    "Authorization": f"Bearer {settings.WHATSAPP_ACCESS_TOKEN}",
    "Content-Type": "application/json",
}


async def send_whatsapp_template(
    to: str,
    guest_name: str,
    event_name: str,
    invite_link: str,
) -> dict:
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "template",
        "template": {
            "name": "invite_notification",
            "language": {"code": "en_US"},
            "components": [
                {
                    "type": "body",
                    "parameters": [
                        {"type": "text", "text": guest_name},
                        {"type": "text", "text": event_name},
                        {"type": "text", "text": invite_link},
                    ],
                }
            ],
        },
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(BASE_WHATSAPP_URL, headers=HEADERS, json=payload)
        response.raise_for_status()
        return response.json()
