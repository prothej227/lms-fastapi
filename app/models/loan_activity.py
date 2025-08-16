from sqlalchemy import Integer, Numeric, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped
from datetime import datetime
from app.database import Base
from decimal import Decimal
from zoneinfo import ZoneInfo
from app.core.config import get_settings


class LoanActivity(Base):
    __tablename__ = "loan_activities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    loan_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("loans.id"), nullable=False
    )
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    activity_type: Mapped[str] = mapped_column(
        String(50), nullable=False
    )  # e.g., 'Payment', 'Penalty', etc.
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    balance_after: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(ZoneInfo(get_settings().timezone)),
        nullable=False,
    )
    loan = relationship("Loan", back_populates="loan_activities")

    def __repr__(self):
        return f"<LoanActivity {self.activity_type} on Loan {self.loan_id}>"
