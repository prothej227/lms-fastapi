from pydantic import BaseModel, Field, ConfigDict, condecimal
from datetime import datetime, date
from typing import Optional

class LoanBase(BaseModel):
    member_id: int = Field(..., example=123)
    amount: condecimal(max_digits=10, decimal_places=2) = Field(..., example="10000.00")  # type: ignore
    interest_rate: condecimal(max_digits=4, decimal_places=2) = Field(..., example="5.25")  # type: ignore
    start_date: date = Field(..., example="2025-08-01")
    end_date: date = Field(..., example="2026-08-01")
    loan_type_id: int = Field(..., example=1)
    status: Optional[int] = Field(default=0, example=0)  # Default to FOR_APPROVAL
    outstanding_balance: condecimal(max_digits=10, decimal_places=2) = Field(..., example="10000.00")  # type: ignore
    total_interest: condecimal(max_digits=10, decimal_places=2) = Field(default=0.00, example="0.00")  # type: ignore
    total_paid: condecimal(max_digits=10, decimal_places=2) = Field(default=0.00, example="0.00")  # type: ignore
    description: Optional[str] = Field(default=None, example="Monthly personal loan")

class LoanCreate(LoanBase):
    created_by_id: int
    modified_by_id: int

class LoanUpdate(BaseModel):
    amount: Optional[condecimal(max_digits=10, decimal_places=2)] = None # type: ignore
    interest_rate: Optional[condecimal(max_digits=4, decimal_places=2)] = None # type: ignore
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    loan_type_id: Optional[int] = None
    status: Optional[int] = None
    outstanding_balance: Optional[condecimal(max_digits=10, decimal_places=2)] = None # type: ignore
    total_interest: Optional[condecimal(max_digits=10, decimal_places=2)] = None # type: ignore
    total_paid: Optional[condecimal(max_digits=10, decimal_places=2)] = None # type: ignore
    description: Optional[str] = None
    modified_by_id: Optional[int] = None

class LoanView(LoanBase):
    id: int
    created_by_id: int
    modified_by_id: int
    created_at: datetime
    modified_at: datetime

    model_config = ConfigDict(from_attributes=True)