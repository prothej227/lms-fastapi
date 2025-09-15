from sqlalchemy import Enum, Integer, Numeric, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped
from datetime import datetime
from app.database import Base
from decimal import Decimal
from zoneinfo import ZoneInfo
from app.core.config import get_settings
from app.core.enums import LoanActivityType, LoanActivityStatus
import uuid


def generate_code() -> str:
    return f"LA-{uuid.uuid4().hex[:8].upper()}"


class LoanActivity(Base):

    __tablename__ = "loan_activities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    loan_activity_code: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False, default=generate_code
    )
    # Link back to the loan
    loan_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("loans.id"), nullable=False
    )

    # Type of activity (enum for consistency)
    activity_type: Mapped[int] = mapped_column(Integer, nullable=False)

    # Transaction details
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    principal_component: Mapped[Decimal] = mapped_column(
        Numeric(12, 2), default=Decimal("0.00"), nullable=False
    )
    interest_component: Mapped[Decimal] = mapped_column(
        Numeric(12, 2), default=Decimal("0.00"), nullable=False
    )
    penalty_component: Mapped[Decimal] = mapped_column(
        Numeric(12, 2), default=Decimal("0.00"), nullable=False
    )

    # Metadata
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    balance_after: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)

    # Optional: link to accounting/GL later
    # gl_entry_id: Mapped[int] = mapped_column(
    #     Integer, ForeignKey("general_ledger.id"), nullable=True
    # )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(ZoneInfo(get_settings().timezone)),
        nullable=False,
    )

    status: Mapped[int] = mapped_column(
        Integer,
        default=LoanActivityStatus.PENDING.value,
        nullable=False,
    )
    # Lifecycle:
    # - Pending   = recorded but not yet approved
    # - Approved  = validated by an admin/manager
    # - Rejected  = denied, will never reach GL
    # - Posted    = moved into GeneralLedger (finalized)

    approved_by: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=True
    )
    approved_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    posted_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    posted_by: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=True
    )
    is_posted: Mapped[bool] = mapped_column(default=False, nullable=False)
    notes: Mapped[str] = mapped_column(String(255), nullable=True)
    reference_number: Mapped[str] = mapped_column(String(100), nullable=True)
    member_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("members.id"), nullable=False
    )

    # Relationships
    loan = relationship("Loan", back_populates="loan_activities")

    def __repr__(self):
        return f"<LoanActivity {self.activity_type} on Loan {self.loan_id}>"
