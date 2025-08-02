from pydantic import BaseModel, EmailStr, Field
from pydantic import field_validator
import re
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr = Field(..., example="john.doe@domain.com")
    username: str = Field(..., min_length=3, max_length=80, example="johndoe")
    role: str = Field(..., example="admin")  # e.g., "admin", "user", "manager"
    password: str = Field(..., min_length=8, example="strongpassword")
    is_active: bool = Optional[Field(..., example="true")]

    @classmethod
    @field_validator('password')
    def validate_password(cls, v):
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter.')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter.')
        if not re.search(r'[0-9]', v):
            raise ValueError('Password must contain at least one digit.')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError('Password must contain at least one special character.')
        return v

class UserLogin(BaseModel):
    username: str = Field(..., min_length=3, max_length=80, example="johndoe")
    password: str = Field(..., min_length=8, example="strongpassword")

    class Config:
        from_attributes = True

class UserView(BaseModel):
    id: int = Field(..., example=1)
    email: EmailStr = Field(..., example="john.doe@domain.com")
    username: str = Field(..., min_length=3, max_length=80, example="johndoe")
    role: str = Field(..., example="admin")
    is_active: Optional[bool] = Field(None, example=True)
    full_name: Optional[str] = Field(None, example="John Doe")

    class Config:
        from_attributes = True
