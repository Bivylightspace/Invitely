import enum
from typing import Annotated
from pydantic import BaseModel, Field, EmailStr, ConfigDict, field_validator
import re 

class UserCreate(BaseModel):
    # Field constraints & metadata for Pydantic v2
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(
        min_length=2, 
        max_length=50, 
        pattern=r"^[A-Za-z\s'-]+$",
        description="User's real name. Allows letters, spaces, hyphens, and apostrophes."
    )
    
    email: EmailStr             
    password:str = Field(
        min_length=8, 
        max_length=42,    
        description="Must include uppercase, lowercase, number, and special character."
    ) 

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):

        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")

        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain an uppercase letter")

        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain a lowercase letter")

        if not re.search(r"\d", v):
            raise ValueError("Password must contain a number")

        if not re.search(r"[@$!%*?&]", v):
            raise ValueError("Password must contain a special character")

        return v
    

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: str
    username: str
    email: EmailStr

    class Config:
        from_attributes = True


class AuthProvider(str, enum.Enum):
    GOOGLE = "google"
    APPLE = "apple"
    EMAIL = "email" 