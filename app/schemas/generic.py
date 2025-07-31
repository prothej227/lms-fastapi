# app/schemas/generic.py - For generic messages
from pydantic import BaseModel
from app.schemas.user import UserView

class GenericResponse(BaseModel):
    status_code: int
    message: str

    class Config:
        extra = "allow"

class LoginResponse(BaseModel):
    message: str
    access_token: str
    user: UserView