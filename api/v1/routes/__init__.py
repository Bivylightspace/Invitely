from fastapi import APIRouter

from api.v1.routes.auth_route import auth_router
from api.v1.routes.invite_route import invite_router
from api.v1.routes.whatsapp_route import whatsapp_router

api_version_one = APIRouter(prefix="/api/v1")
api_version_one.include_router(auth_router, tags=["Authentication"])
api_version_one.include_router(invite_router, tags=["Invites"])
api_version_one.include_router(whatsapp_router, tags=["WhatsApp"])
 