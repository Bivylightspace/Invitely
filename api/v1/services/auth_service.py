from fastapi import HTTPException
from api.utils.hashing import verify_password
from sqlalchemy.orm import Session
from api.v1.schemas.user import UserCreate, UserLogin
from api.v1.models.user import User
from api.v1.models.auth_account import AuthAccount, AuthProvider
from api.utils.hashing import hash_password
from api.utils.jwt_handler import create_access_token 

def register_user(user_data: UserCreate, db: Session) -> dict:
    # 1. Create the base User profile
    new_user = User(
        name=user_data.name,
        # phone=user_data.phone  # Add this if you added phone to your schema
    )
    
    db.add(new_user)
    db.flush()  # Use flush to get the new_user.id without committing the transaction yet

    # 2. Create the AuthAccount (The 'email' credential)
    new_auth = AuthAccount(
        provider=AuthProvider.EMAIL,
        provider_id=user_data.email, # For email auth, the ID is usually the email
        email=user_data.email,
        password_hash=hash_password(user_data.password),
        user_id=new_user.id
    )
    
    db.add(new_auth)
    
    try:
        db.commit() # Atomic commit: both User and AuthAccount are saved or neither is
        db.refresh(new_user)
    except Exception as e:
        db.rollback() # If something fails (like a duplicate email), undo everything
        raise e
    return new_user
    
def login_user(user_data: UserLogin, db: Session):
    auth_account = db.query(AuthAccount).filter(AuthAccount.email == user_data.email).first()
    if not verify_password(user_data.password, auth_account.password_hash):
        raise HTTPException(status_code=401, detail="Unsuccessful Login!")
    access_token = create_access_token(
        user_id=auth_account.user_id, email=user_data.email
    )
    return {
        "access_token": access_token,
    }