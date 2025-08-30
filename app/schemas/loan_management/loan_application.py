from datetime import datetime
from zoneinfo import ZoneInfo
from decimal import Decimal
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict
from app.models.loan import LoanStatus
from app.core.config import get_settings
from app.models import LoanApplication
from app.core.enums import LoanApplicationStatus


class LoanApplicationBase(BaseModel):
    member_id: int = Field(..., examples=[101])
    loan_type_id: int = Field(..., examples=[5])
    amount_requested: Decimal = Field(..., examples=["50000.00"])
    application_date: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(ZoneInfo(get_settings().timezone)),
    )
    status: int = Field(..., examples=[LoanStatus.FOR_APPROVAL])


class LoanApplicationCreate(LoanApplicationBase):
    pass


class LoanApplicationUpdate(BaseModel):
    member_id: Optional[int] = Field(None, examples=[102])
    loan_type_id: Optional[int] = Field(None, examples=[6])
    amount_requested: Optional[Decimal] = Field(None, examples=["75000.00"])
    application_date: Optional[datetime] = Field(
        None, examples=["2025-08-11T14:45:00Z"]
    )
    status: Optional[int] = Field(None, examples=[2])
    loan_id: Optional[int] = Field(None, examples=[2001])


class LoanApplicationRequestFilters(BaseModel):
    status: Optional[int] = None


class LoanApplicationView(LoanApplicationBase):
    id: int = Field(..., examples=[1001])
    loan_id: Optional[int] = Field(None, examples=[2000])
    loan_type_name: Optional[str] = Field("", examples=["Personal Loan"])
    member_name: Optional[str] = Field(default="Unknown Member", examples=["John Doe"])
    model_config = ConfigDict(from_attributes=True)
    status: str | int = Field("Unknown Status")

    @classmethod
    def from_orm_with_names(
        cls, loan_application: LoanApplication
    ) -> "LoanApplicationView":
        return cls(
            id=loan_application.id,
            member_id=loan_application.member_id,
            member_name=(
                loan_application.member.name
                if loan_application.member
                else "Unknown Member"
            ),
            loan_type_id=loan_application.loan_type_id,
            amount_requested=loan_application.amount_requested,
            loan_type_name=(
                loan_application.loan_type.name
                if loan_application.loan_type
                else "Unknown Loan Type"
            ),
            application_date=loan_application.application_date,
            status=(
                LoanApplicationStatus(loan_application.status).get_proper_name()
                if loan_application.status
                else "Unknown Status"
            ),
            loan_id=loan_application.loan_id,
        )


class LoanApplicationResponseWithCount(BaseModel):
    total_count: int
    records: List[LoanApplicationView]
