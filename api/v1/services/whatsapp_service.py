import httpx
from api.utils.config import settings


HEADERS = {
    "Authorization": f"Bearer {settings.WHATSAPP_ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

async def send_invite_notification(to: str, guest_name: str, event_name: str, invite_link: str):
    """Send an invite notification via WhatsApp"""
    payload = {
        "messaging_product": "whatsapp",
        "to": to,  # format: 2348XXXXXXXXX or +2347XXXXXXXXXXX
        "type": "template",
        "template": {
        "name": "invite_notification",
        "language": {"code": "en"},
        "components": [
            {
                "type": "body",
                "parameters": [
                    {"type": "text", "text": guest_name},
                    {"type": "text", "text": event_name},
                    {"type": "link", "text": invite_link}
                ]
            }
        ]
    }
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(settings.WHATSAPP_BASE_URL, headers=HEADERS, json=payload)
        print("Status:", response.status_code)
        print("Response:", response.text)
        response.raise_for_status()
        return response.json()