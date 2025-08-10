from datetime import date
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class BeneficiaryBase(BaseModel):
    member_id: int = Field(..., examples=[1])
    full_name: str = Field(..., examples=["Jane Doe"])
    relationship_type: str = Field(..., examples=["Spouse"])
    dob: date = Field(..., examples=["1990-05-15"])
    occupation: Optional[str] = Field(None, examples=["Teacher"])
    employer: Optional[str] = Field(None, examples=["Springfield Elementary"])


class BeneficiaryCreate(BeneficiaryBase):
    """Fields required for creating a Beneficiary"""

    pass


class BeneficiaryNestedCreate(BaseModel):
    full_name: str = Field(..., examples=["Jane Doe"])
    relationship_type: str = Field(..., examples=["Spouse"])
    dob: date = Field(..., examples=["1990-05-15"])
    occupation: Optional[str] = Field(None, examples=["Teacher"])
    employer: Optional[str] = Field(None, examples=["Springfield Elementary"])


class BeneficiaryUpdate(BaseModel):
    """All fields optional for partial updates"""

    full_name: Optional[str] = Field(None, examples=["Jane A. Doe"])
    relationship_type: Optional[str] = Field(None, examples=["Mother"])
    dob: Optional[date] = Field(None, examples=["1975-02-20"])
    occupation: Optional[str] = Field(None, examples=["Nurse"])
    employer: Optional[str] = Field(None, examples=["City Hospital"])


class BeneficiaryView(BeneficiaryBase):
    id: int = Field(..., examples=[101])

    model_config = ConfigDict(from_attributes=True)
