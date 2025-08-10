from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, Field
from typing import List
from .beneficiary import BeneficiaryNestedCreate


class MemberBase(BaseModel):
    first_name: str = Field(..., max_length=255, examples=["Juan"])
    middle_name: Optional[str] = Field(None, max_length=255, examples=["Reyes"])
    last_name: str = Field(..., max_length=255, examples=["Dela Cruz"])
    birth_address: str = Field(..., max_length=255, examples=["123 Mabini St, Manila"])
    dob: date = Field(..., examples=["1990-05-15"])
    nationality: str = Field(..., max_length=255, examples=["Filipino"])
    religion: str = Field(..., max_length=255, examples=["Roman Catholic"])
    sex: str = Field(..., max_length=6, examples=["Male"])
    civil_status: str = Field(..., max_length=50, examples=["Single"])
    current_address: str = Field(
        ..., max_length=255, examples=["456 Rizal Ave, Quezon City"]
    )
    permanent_address: str = Field(
        ..., max_length=255, examples=["789 Bonifacio St, Cebu City"]
    )
    contact_number: str = Field(..., max_length=20, examples=["+63 912 345 6789"])
    zip_code: str = Field(..., max_length=10, examples=["1001"])
    tin_number: Optional[str] = Field(None, max_length=40, examples=["123-456-789-000"])
    id_type1: str = Field(..., max_length=25, examples=["PhilHealth"])
    id_type2: Optional[str] = Field(None, max_length=25, examples=["SSS"])
    id_number1: str = Field(..., max_length=30, examples=["PH123456789"])
    id_number2: Optional[str] = Field(None, max_length=30, examples=["SSS987654321"])
    basic_education: Optional[str] = Field(
        None, max_length=255, examples=["High School Diploma"]
    )
    vocational_degree: Optional[str] = Field(
        None, max_length=255, examples=["Welding NCII"]
    )
    college_degree: Optional[str] = Field(
        None, max_length=255, examples=["BS Computer Science"]
    )
    pos_grad_degree: Optional[str] = Field(None, max_length=255, examples=["MBA"])
    occupation: Optional[str] = Field(None, max_length=10, examples=["Engineer"])


class MemberCreate(MemberBase):
    created_by_id: int = Field(..., examples=[1])
    modified_by_id: int = Field(..., examples=[1])
    beneficiaries: Optional[List[BeneficiaryNestedCreate]]


class MemberUpdate(BaseModel):
    first_name: Optional[str] = Field(None, max_length=255, examples=["Juan"])
    middle_name: Optional[str] = Field(None, max_length=255, examples=["Reyes"])
    last_name: Optional[str] = Field(None, max_length=255, examples=["Dela Cruz"])
    birth_address: Optional[str] = Field(
        None, max_length=255, examples=["123 Mabini St, Manila"]
    )
    dob: Optional[date] = Field(None, examples=["1990-05-15"])
    nationality: Optional[str] = Field(None, max_length=255, examples=["Filipino"])
    religion: Optional[str] = Field(None, max_length=255, examples=["Roman Catholic"])
    sex: Optional[str] = Field(None, max_length=6, examples=["Male"])
    civil_status: Optional[str] = Field(None, max_length=50, examples=["Single"])
    current_address: Optional[str] = Field(
        None, max_length=255, examples=["456 Rizal Ave, Quezon City"]
    )
    permanent_address: Optional[str] = Field(
        None, max_length=255, examples=["789 Bonifacio St, Cebu City"]
    )
    contact_number: Optional[str] = Field(
        None, max_length=20, examples=["+63 912 345 6789"]
    )
    zip_code: Optional[str] = Field(None, max_length=10, examples=["1001"])
    tin_number: Optional[str] = Field(None, max_length=40, examples=["123-456-789-000"])
    id_type1: Optional[str] = Field(None, max_length=25, examples=["PhilHealth"])
    id_type2: Optional[str] = Field(None, max_length=25, examples=["SSS"])
    id_number1: Optional[str] = Field(None, max_length=30, examples=["PH123456789"])
    id_number2: Optional[str] = Field(None, max_length=30, examples=["SSS987654321"])
    basic_education: Optional[str] = Field(
        None, max_length=255, examples=["High School Diploma"]
    )
    vocational_degree: Optional[str] = Field(
        None, max_length=255, examples=["Welding NCII"]
    )
    college_degree: Optional[str] = Field(
        None, max_length=255, examples=["BS Computer Science"]
    )
    pos_grad_degree: Optional[str] = Field(None, max_length=255, examples=["MBA"])
    occupation: Optional[str] = Field(None, max_length=10, examples=["Engineer"])
    modified_by_id: Optional[int] = Field(None, examples=[2])


class MemberView(MemberBase):
    id: int = Field(..., examples=[101])
    created_by_id: int = Field(..., examples=[1])
    created_at: datetime = Field(..., examples=["2025-08-10T10:30:00Z"])
    modified_by_id: int = Field(..., examples=[2])
    modified_at: datetime = Field(..., examples=["2025-08-10T10:45:00Z"])

    model_config = {"from_attributes": True}
