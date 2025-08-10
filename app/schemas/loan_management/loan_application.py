from datetime import datetime
from zoneinfo import ZoneInfo
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from app.models.loan import LoanStatus
from app.core.config import get_settings


class LoanApplicationBase(BaseModel):
    member_id: int = Field(..., examples=[101])
    loan_type_id: int = Field(..., examples=[5])
    amount_requested: Decimal = Field(..., examples=["50000.00"])
    application_date: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(ZoneInfo(get_settings().timezone)),
    )
    status: int = Field(
        ..., examples=[LoanStatus.FOR_APPROVAL]
    )  # Could be replaced with Enum for LoanStatus


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


class LoanApplicationView(LoanApplicationBase):
    id: int = Field(..., examples=[1001])
    loan_id: Optional[int] = Field(None, examples=[2000])

    model_config = ConfigDict(from_attributes=True)
