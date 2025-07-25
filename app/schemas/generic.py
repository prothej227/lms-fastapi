# app/schemas/generic.py - For generic messages
from pydantic import BaseModel

class GenericResponse(BaseModel):
    status_code: int
    message: str

    class Config:
        extra = "allow"