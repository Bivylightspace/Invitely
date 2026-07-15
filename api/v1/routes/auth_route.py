from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.db.database import get_db 
from api.v1.schemas.user import UserCreate, UserLogin, UserResponse
from api.v1.services.auth_service import register_user, login_user
from api.utils.responses import success_response, fail_response, auth_response

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

# HTTP Verb 
@auth_router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):  
    new_user = register_user(user, db)
    return success_response(
        status_code=200,
        message="User Registered Successfully!",
        data=new_user
    )    

@auth_router.post("/login")
def login(loginDetails: UserLogin, db: Session = Depends(get_db)):
    login_data = login_user(loginDetails, db)
    return success_response(
        status_code=200,
        message="Login Successful!",
        data=login_data
    )                          
