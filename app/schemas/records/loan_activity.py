from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field
from typing import Optional, List
from app.core.enums import LoanActivityType, LoanActivityStatus


class LoanActivityBase(BaseModel):
    loan_id: int
    member_id: str = Field(..., description="Member ID of the payee")
    activity_type: int = Field(
        ...,
        description="Type of loan activity (1=Disbursement, 2=Payment, 3=Penalty, 4=Interest, 5=Adjustment, 6=Write-Off)",
        examples=[1, 2, 3, 4, 5, 6],
    )
    amount: Decimal = Field(..., description="Total amount of the loan activity")
    principal_component: Decimal = Decimal("0.00")
    interest_component: Decimal = Decimal("0.00")
    penalty_component: Decimal = Decimal("0.00")
    description: Optional[str] = Field(
        None, description="Description of the loan activity"
    )
    balance_after: Decimal = Field(..., description="Loan balance after this activity")
    status: int = Field(
        LoanActivityStatus.PENDING.value, description="Status of the loan activity"
    )
    is_posted: bool = Field(
        False, description="Indicates if the activity has been posted to the ledger"
    )
    reference_number: Optional[str] = Field(
        None, description="Reference number for the activity"
    )
    notes: Optional[str] = Field(
        None, description="Additional notes about the loan activity"
    )


class LoanActivityCreate(LoanActivityBase):
    pass


class LoanActivityUpdate(BaseModel):
    activity_type: Optional[LoanActivityType] = None
    amount: Optional[Decimal] = None
    principal_component: Optional[Decimal] = None
    interest_component: Optional[Decimal] = None
    penalty_component: Optional[Decimal] = None
    description: Optional[str] = None
    balance_after: Optional[Decimal] = None
    status: Optional[LoanActivityStatus] = None
    approved_by: Optional[int] = None
    approved_at: Optional[datetime] = None
    posted_at: Optional[datetime] = None


class LoanActivityRead(LoanActivityBase):
    id: int
    loan_activity_code: str
    created_at: datetime
    approved_by: Optional[int] = None
    approved_at: Optional[datetime] = None
    posted_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class LoanActivityResponseWithCount(BaseModel):
    total_count: int
    records: List[LoanActivityRead]


class LoanActivityRequestFilters(BaseModel):
    member_id: Optional[str] = None
