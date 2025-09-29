from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, Field
from typing import List
from .beneficiary import BeneficiaryNestedCreate
from app.models import Member


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
    beneficiaries: Optional[List[BeneficiaryNestedCreate]] = None


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


class MemberCreateResponseView(BaseModel):
    message: str = Field(..., examples=["Member created successfully."])
    member_id: int = Field(..., examples=[101])


class MemberView(MemberBase):
    id: int = Field(..., examples=[101])
    member_id: str
    created_by: str = ""
    created_at: datetime = Field(..., examples=["2025-08-10T10:30:00Z"])
    modified_by: str = ""
    modified_at: datetime = Field(..., examples=["2025-08-10T10:45:00Z"])

    model_config = {"from_attributes": True}

    @classmethod
    def from_orm_with_names(cls, member: Member) -> "MemberView":
        return cls(
            id=member.id,
            member_id=member.member_id,
            first_name=member.first_name,
            middle_name=member.middle_name,
            last_name=member.last_name,
            birth_address=member.birth_address,
            dob=member.dob,
            nationality=member.nationality,
            religion=member.religion,
            sex=member.sex,
            civil_status=member.civil_status,
            current_address=member.current_address,
            permanent_address=member.permanent_address,
            contact_number=member.contact_number,
            zip_code=member.zip_code,
            tin_number=member.tin_number,
            id_type1=member.id_type1,
            id_type2=member.id_type2,
            id_number1=member.id_number1,
            id_number2=member.id_number2,
            basic_education=member.basic_education,
            vocational_degree=member.vocational_degree,
            college_degree=member.college_degree,
            pos_grad_degree=member.pos_grad_degree,
            occupation=member.occupation,
            created_by=(
                member.created_by.first_name + " " + member.created_by.last_name
                if member.created_by
                else ""
            ),
            created_at=member.created_at,
            modified_by=(
                member.modified_by.first_name + " " + member.modified_by.last_name
                if member.modified_by
                else ""
            ),
            modified_at=member.modified_at,
        )


class MemberResponseWithCount(BaseModel):
    total_count: int
    records: List[MemberView]


class MemberRequestFilters(BaseModel):
    name: Optional[str] = None
    is_active: Optional[bool] = None
