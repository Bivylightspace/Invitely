from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api.db.database import get_db
from api.v1.schemas.user_schema import UserCreate, UserLogin, UserResponse
from api.v1.services.auth_service import login_user, register_user


router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    new_user = register_user(user, db)
    if not new_user:
        raise HTTPException(status_code=400, detail="Username already taken")
    return new_user

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):  
    token = login_user(user.username, user.password, db)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return {"access_token": token, "token_type": "bearer"}
