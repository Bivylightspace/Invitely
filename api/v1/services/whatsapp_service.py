import httpx
import os
from api.utils.config import settings


BASE_URL = f"https://graph.facebook.com/v25.0/{settings.WHATSAPP_PHONE_NUMBER_ID}/messages"

HEADERS = {
    "Authorization": f"Bearer {settings.WHATSAPP_ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

async def send_invite_notification(to: str, guest_name: str, event_name: str, invite_link: str):
    """Send an invite notification via WhatsApp"""
    payload = {
        "messaging_product": "whatsapp",
        "to": to,  # format: 2348XXXXXXXXX
        "type": "template",
        "template": {
            "name": "hello_world",
            # "name": f"hello, {guest_name}, you're invited to {event_name}! Click here to RSVP: {invite_link}",  # replace with your custom template later
            "language": {"code": "en_US"},
        }
    #     "template": {
    #     "name": "invite_notification",
    #     "language": {"code": "en"},
    #     "components": [
    #         {
    #             "type": "body",
    #             "parameters": [
    #                 {"type": "text", "text": guest_name},
    #                 {"type": "text", "text": event_name},
    #                 {"type": "text", "text": invite_link}
    #             ]
    #         }
    #     ]
    # }
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(BASE_URL, headers=HEADERS, json=payload)
        print("Status:", response.status_code)
        print("Response:", response.text)
        response.raise_for_status()
        return response.json()