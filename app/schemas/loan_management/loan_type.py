from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional, Any
from app.models.loan_type import LoanType
from app.utils.helpers import get_enum_label
from app.core.enums import PaymentFrequency, AmortizationType


class LoanTypeBase(BaseModel):
    name: str = Field(..., max_length=50, description="Name of the loan type")
    interest_rate: float = Field(..., description="Set interest rate (%)")
    term_months: int = Field(..., description="Total term of the loan in months")
    payment_frequency: Optional[int] = Field(..., description="Payment frequency code")
    amortization_type: Optional[int] = Field(..., description="Amortization type code")
    grace_period_months: int = Field(
        0, description="Number of months before first payment is due"
    )
    penalty_rate: float = Field(
        0.0, description="Penalty interest rate (%) for late payments"
    )
    description: Optional[str] = Field(
        None, max_length=255, description="Description of the loan type"
    )
    is_active: bool = Field(True, description="Is the loan type active?")


class LoanTypeCreate(LoanTypeBase):
    created_by_id: int = Field(..., description="ID of the user creating the loan type")


class LoanTypeUpdate(BaseModel):
    name: Optional[str] = Field(
        None, max_length=50, description="Updated name of the loan type"
    )
    interest_rate: Optional[float] = Field(
        None, description="Updated interest rate (%)"
    )
    term_months: Optional[int] = Field(None, description="Updated term in months")
    payment_frequency: Optional[int] = Field(
        None, description="Updated payment frequency code"
    )
    amortization_type: Optional[int] = Field(
        None, description="Updated amortization type code"
    )
    grace_period_months: Optional[int] = Field(
        None, description="Updated grace period in months"
    )
    penalty_rate: Optional[float] = Field(
        None, description="Updated penalty interest rate (%)"
    )
    description: Optional[str] = Field(
        None, max_length=255, description="Updated description"
    )
    is_active: Optional[bool] = Field(None, description="Update active status")
    modified_by_id: int = Field(
        ..., description="ID of the user modifying the loan type"
    )


class LoanTypeInDB(LoanTypeBase):
    id: int
    created_by_id: int
    modified_by_id: Optional[int]
    created_at: datetime
    modified_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)


class LoanTypeResponse(LoanTypeBase):
    id: int
    created_by_name: Optional[str]
    modified_by_name: Optional[str]
    created_at: datetime
    modified_at: Optional[datetime]
    payment_frequency: Optional[str | int]
    amortization_type: Optional[str | int]
    model_config = ConfigDict(from_attributes=True)
    is_active: str | bool

    @classmethod
    def from_orm_with_names(cls, loan_type: LoanType) -> "LoanTypeResponse":
        return cls(
            id=loan_type.id,
            name=loan_type.name,
            interest_rate=loan_type.interest_rate,
            term_months=loan_type.term_months,
            payment_frequency=get_enum_label(
                PaymentFrequency, loan_type.payment_frequency
            ),
            amortization_type=get_enum_label(
                AmortizationType, loan_type.amortization_type
            ),
            grace_period_months=loan_type.grace_period_months,
            penalty_rate=loan_type.penalty_rate,
            description=loan_type.description,
            is_active="Yes" if loan_type.is_active else "No",
            created_by_name=(
                f"{loan_type.created_by.first_name} {loan_type.created_by.last_name}"
                if loan_type.created_by
                else None
            ),
            modified_by_name=(
                f"{loan_type.modified_by.first_name} {loan_type.modified_by.last_name}"
                if loan_type.modified_by
                else None
            ),
            created_at=loan_type.created_at,
            modified_at=loan_type.modified_at,
        )


class LoanTypeFilter(BaseModel):
    label: str
    value: int

    @classmethod
    def from_orm_label_value(cls, loan_type: LoanType) -> "LoanTypeFilter":
        return cls(label=loan_type.name, value=loan_type.id)
