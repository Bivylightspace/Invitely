from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api.db.database import get_db
from api.v1.schemas.user_schema import UserCreate, UserLogin
from api.v1.services.auth_service import login_user, register_user

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    new_user = register_user(user, db)
    if not new_user:
        raise HTTPException(
            status_code=400, detail="Account with this email already exists"
        )
    user_data = {
        "id": str(new_user.id),
        "name": new_user.name,
        "username": new_user.username,
        "email": new_user.email,
    }
    return {
        "status": "success",
        "status_code": 201,
        "message": "Account created successfully!",
        "data": user_data,
        **user_data,
    }


@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    auth_data = login_user(user.email, user.password, db)
    if not auth_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )
    token = auth_data["access_token"]
    user_info = auth_data["user"]
    return {
        "status": "success",
        "status_code": 200,
        "message": "Login successful",
        "access_token": token,
        "token_type": "bearer",
        "data": {
            "access_token": token,
            "token_type": "bearer",
            "user": user_info,
        },
    }
