from sqlalchemy.orm import Session

from api.utils.hashing import hash_password, verify_password
from api.utils.jwt_handler import create_access_token
from api.v1.models.auth_account import AuthAccount
from api.v1.models.user import User
from api.v1.schemas.user_schema import UserCreate


def register_user(user_data: UserCreate, db: Session):
    existing_account = (
        db.query(AuthAccount).filter(AuthAccount.email == user_data.email).first()
    )
    if existing_account:
        return None

    user_name = (
        getattr(user_data, "name", None)
        or getattr(user_data, "username", None)
        or str(user_data.email)
    )
    new_user = User(name=user_name)
    db.add(new_user)
    db.flush()

    auth_account = AuthAccount(
        user_id=new_user.id,
        provider="local",
        provider_id=str(user_data.email),
        email=str(user_data.email),
        password_hash=hash_password(user_data.password),
    )
    db.add(auth_account)
    db.commit()
    db.refresh(new_user)
    return new_user


def login_user(email: str, password: str, db: Session):
    auth_account = db.query(AuthAccount).filter(AuthAccount.email == email).first()
    if (
        not auth_account
        or not auth_account.password_hash
        or not verify_password(password, auth_account.password_hash)
    ):
        return None
    token = create_access_token(
        {"sub": auth_account.email, "user_id": str(auth_account.user_id)}
    )
    return token
