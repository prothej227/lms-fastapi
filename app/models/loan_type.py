from sqlalchemy import Integer, String, DateTime, ForeignKey, Numeric, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from app.database import Base
from typing import Optional
from app.core.config import get_settings
from zoneinfo import ZoneInfo
from app.core.enums import PaymentFrequency, AmortizationType


class LoanType(Base):
    __tablename__ = "loan_types"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    interest_rate: Mapped[float] = mapped_column(Numeric(4, 2), nullable=False)
    term_months: Mapped[int] = mapped_column(Integer, nullable=False)

    # Changed from String -> Integer (reference to config)
    payment_frequency: Mapped[int] = mapped_column(
        Integer, nullable=False, default=PaymentFrequency.MONTHLY
    )
    amortization_type: Mapped[int] = mapped_column(
        Integer, nullable=False, default=AmortizationType.EQUAL_INSTALLMENTS
    )

    grace_period_months: Mapped[int] = mapped_column(Integer, default=0)
    penalty_rate: Mapped[float] = mapped_column(Numeric(4, 2), default=0.0)
    description: Mapped[Optional[str]] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    created_by_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    modified_by_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(ZoneInfo(get_settings().timezone)),
        nullable=False,
    )
    modified_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime, onupdate=lambda: datetime.now(ZoneInfo(get_settings().timezone))
    )

    created_by = relationship("User", foreign_keys=[created_by_id])
    modified_by = relationship("User", foreign_keys=[modified_by_id])
    loans = relationship("Loan", back_populates="loan_type")

    def __repr__(self) -> str:
        return f"<LoanType {self.name}>"
