from pydantic import BaseModel, Field, ConfigDict, condecimal
from datetime import datetime, date
from typing import Optional, List
from app.models import Loan
from app.core import enums


class LoanBase(BaseModel):
    member_id: int = Field(..., example=123)  # type: ignore
    amount: condecimal(max_digits=10, decimal_places=2) = Field(..., example="10000.00")  # type: ignore
    interest_rate: condecimal(max_digits=4, decimal_places=2) = Field(..., example="5.25")  # type: ignore
    start_date: date = Field(..., example="2025-08-01")  # type: ignore
    end_date: date = Field(..., example="2026-08-01")  # type: ignore
    status: Optional[int] = Field(default=enums.LoanStatus.PENDING)  # type: ignore
    outstanding_balance: condecimal(max_digits=10, decimal_places=2) = Field(..., example="10000.00")  # type: ignore
    total_interest: condecimal(max_digits=10, decimal_places=2) = Field(default=0.00, example="0.00")  # type: ignore
    total_paid: condecimal(max_digits=10, decimal_places=2) = Field(default=0.00, example="0.00")  # type: ignore
    description: Optional[str] = Field(default=None, example="Monthly personal loan")  # type: ignore
    loan_type_id: int = Field(..., example=1)  # type: ignore


class LoanCreate(LoanBase):
    created_by_id: int
    modified_by_id: Optional[int]


class LoanUpdate(BaseModel):
    amount: Optional[condecimal(max_digits=10, decimal_places=2)] = None  # type: ignore
    interest_rate: Optional[condecimal(max_digits=4, decimal_places=2)] = None  # type: ignore
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    loan_type_id: Optional[int] = None
    status: Optional[int] = None
    outstanding_balance: Optional[condecimal(max_digits=10, decimal_places=2)] = None  # type: ignore
    total_interest: Optional[condecimal(max_digits=10, decimal_places=2)] = None  # type: ignore
    total_paid: Optional[condecimal(max_digits=10, decimal_places=2)] = None  # type: ignore
    description: Optional[str] = None
    modified_by_id: Optional[int] = None


class LoanView(LoanBase):
    id: int
    status: str | int = ""
    loan_type_name: Optional[str]
    created_by_name: Optional[str]
    modified_by_name: Optional[str]
    created_at: datetime
    modified_at: datetime
    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_orm_with_names(cls, loan: Loan) -> "LoanView":
        return cls(
            id=loan.id,
            member_id=loan.member_id,
            amount=loan.amount,
            interest_rate=loan.interest_rate,
            start_date=loan.start_date,
            end_date=loan.end_date,
            loan_type_id=loan.loan_type_id,
            loan_type_name=loan.loan_type.name,
            status=(
                enums.LoanStatus(loan.status).get_proper_name()
                if loan.status is not None
                else ""
            ),
            outstanding_balance=loan.outstanding_balance,
            total_interest=loan.total_interest,
            total_paid=loan.total_paid,
            description=loan.description,
            created_by_name=(
                f"{loan.created_by.first_name} {loan.created_by.last_name}"
                if loan.created_by
                else ""
            ),
            modified_by_name=(
                f"{loan.modified_by.first_name} {loan.modified_by.last_name}"
                if loan.modified_by
                else ""
            ),
            created_at=loan.created_at,
            modified_at=loan.modified_at,
        )


class LoanRequestFilters(BaseModel):
    status: Optional[int] = None


class LoanResponseWithCount(BaseModel):
    total_count: int
    records: List[LoanView]
