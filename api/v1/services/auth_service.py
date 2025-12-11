from sqlalchemy.orm import Session
from v1.model.user import User
from schema.user_schema import UserCreate
from utils.hashing import hash_password, verify_password
from utils.jwt_handler import create_access_token

def register_user(user_data: UserCreate, db: Session):
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        return None
    hashed_pwd = hash_password(user_data.password)
    new_user = User(username=user_data.username, email=user_data.email, password=hashed_pwd)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def login_user(username: str, password: str, db: Session):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.password):
        return None
    token = create_access_token({"sub": user.username})
    return token
