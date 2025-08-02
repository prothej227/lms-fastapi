from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class LoanTypeBase(BaseModel):
    name: str = Field(..., max_length=50, description="Name of the loan type")
    description: Optional[str] = Field(None, max_length=255, description="Description of the loan type")

class LoanTypeCreate(LoanTypeBase):
    created_by: int = Optional[Field(..., description="ID of the user creating the loan type")]

class LoanTypeUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=50, description="Updated name of the loan type")
    description: Optional[str] = Field(None, max_length=255, description="Updated description of the loan type")
    modified_by: int = Field(..., description="ID of the user modifying the loan type")

class LoanTypeInDB(LoanTypeBase):
    id: int
    created_by: int
    modified_by: Optional[int]
    created_at: datetime
    modified_at: Optional[datetime]

    class Config:
        orm_mode = True

class LoanTypeResponse(LoanTypeBase):
    id: int
    created_by_name: str
    modified_by_name: Optional[str]
    created_at: datetime
    modified_at: Optional[datetime]

    class Config:
        orm_mode = True

