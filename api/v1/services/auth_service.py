from sqlalchemy.orm import Session

from api.utils.hashing import hash_password, verify_password
from api.utils.jwt_handler import create_access_token
from api.v1.models.user import User
from api.v1.schemas.user_schema import UserCreate


def register_user(user_data: UserCreate, db: Session):
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        return None
    hashed_pwd = hash_password(user_data.password)
    new_user = User(name=user_data.name, email=user_data.email, password=hashed_pwd)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def login_user(username: str, password: str, db: Session):
    user = db.query(User).filter(User.email == username).first()
    if not user or not verify_password(password, user.password):
        return None
    token = create_access_token({"sub": user.email})
    return token
