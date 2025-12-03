from passlib.context import CryptContext

passwordContext = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return passwordContext.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return passwordContext.verify(plain_password, hashed_password)

       