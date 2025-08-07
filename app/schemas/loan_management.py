from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional
from app.models.loan_type import LoanType

class LoanTypeBase(BaseModel):
    name: str = Field(..., max_length=50, description="Name of the loan type")
    description: Optional[str] = Field(
        None, max_length=255, description="Description of the loan type"
    )


class LoanTypeCreate(LoanTypeBase):
    created_by_id: int = Optional[
        Field(..., description="ID of the user creating the loan type")
    ]  # pyright: ignore[reportAssignmentType]


class LoanTypeUpdate(BaseModel):
    name: Optional[str] = Field(
        None, max_length=50, description="Updated name of the loan type"
    )
    description: Optional[str] = Field(
        None, max_length=255, description="Updated description of the loan type"
    )
    modified_by: int = Field(..., description="ID of the user modifying the loan type")


class LoanTypeInDB(LoanTypeBase):
    id: int
    created_by: int
    modified_by: Optional[int]
    created_at: datetime
    modified_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)


class LoanTypeResponse(LoanTypeBase):
    id: int
    created_by_name: Optional[str]
    modified_by_name: Optional[str]
    created_at: datetime
    modified_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_orm_with_names(cls, loan_type: LoanType) -> "LoanTypeResponse":
        return cls(
            id=loan_type.id,
            name=loan_type.name,
            description=loan_type.description,
            created_by_name=f"{loan_type.created_by.first_name} {loan_type.created_by.last_name}" if loan_type.created_by else "",
            modified_by_name=f"{loan_type.modified_by.first_name} {loan_type.modified_by.last_name}" if loan_type.modified_by else None,
            created_at=loan_type.created_at,
            modified_at=loan_type.modified_at,
        )