

from fastapi import APIRouter
from api.v1.routes.auth_route import auth_router
from api.v1.routes.event import event_router   


api_version_one = APIRouter(prefix="/api/v1")      
                                                           
api_version_one.include_router(auth_router, tags=["users"])

api_version_one.include_router(event_router, tags=["events"])