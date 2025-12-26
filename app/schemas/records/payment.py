from pydantic import BaseModel, Field
from decimal import Decimal
from typing import Optional


class PaymentCreate(BaseModel):
    loan_id: int = Field(..., description="Reference Loan ID")
    paymentAmount: Decimal = Field(..., description="Total amount of payment")
    reference_number: Optional[str] = Field(None, description="Member ID of the payee")
    notes: Optional[str] = Field(None, description="Additional payment notes")
