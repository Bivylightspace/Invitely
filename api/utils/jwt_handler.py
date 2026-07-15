from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from typing import Optional
from api.utils.config import settings
           
     

def create_access_token(email: str, user_id: int, expires_delta: int = settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES):
    # 1. Use the subject claim properly (usually the unique identifier/username)
    encode = {"sub": email, "id": user_id}
    
    # 2. Determine expiration: use provided integer or fall back to Settings
    if expires_delta is not None:
        expire_time = expires_delta
    else:
        expire_time = settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        
    expires = datetime.now(timezone.utc) + timedelta(minutes=expire_time)
    
    # 3. Update the claims and encode
    encode.update({"exp": expires})
    
    return jwt.encode(encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

def decode_token(token: str):
    try:                                                                
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except JWTError:
        return None

def token_expired(token: str) -> bool:
    try:                               
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        exp = payload.get("exp")
        return datetime.utcnow() > datetime.fromtimestamp(exp)
    except JWTError:
        return True
