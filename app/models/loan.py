from sqlalchemy import Integer, String, ForeignKey, Numeric, Date, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import date, datetime, timezone
from app.database import Base
from typing import Optional
from decimal import Decimal


class LoanStatus:
    FOR_APPROVAL = 0
    APPROVED = 1
    REJECTED = 2
    DISBURSED = 3
    ACTIVE = 4
    DEFAULTED = 5
    CLOSED = 6

    @classmethod
    def choices(cls):
        return [
            (cls.FOR_APPROVAL, "For Approval"),
            (cls.APPROVED, "Approved"),
            (cls.REJECTED, "Rejected"),
            (cls.DISBURSED, "Disbursed"),
            (cls.ACTIVE, "Active"),
            (cls.DEFAULTED, "Defaulted"),
            (cls.CLOSED, "Closed"),
        ]


class Loan(Base):
    __tablename__ = "loans"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    member_id: Mapped[int] = mapped_column(ForeignKey("members.id"), nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    interest_rate: Mapped[Decimal] = mapped_column(Numeric(4, 2), nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False, default=date.today)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    loan_type_id: Mapped[int] = mapped_column(
        ForeignKey("loan_types.id"), nullable=False
    )
    status: Mapped[int] = mapped_column(
        Integer, nullable=False, default=LoanStatus.FOR_APPROVAL
    )
    outstanding_balance: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    total_interest: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), nullable=False, default=0.00
    )
    total_paid: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), nullable=False, default=0.00
    )
    description: Mapped[Optional[str]] = mapped_column(String(255))
    created_by_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )
    modified_by_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    modified_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )

    # Relationships
    loan_activities = relationship("LoanActivity", back_populates="loan")
    loan_type = relationship("LoanType", back_populates="loans")
    member = relationship("Member", back_populates="loans")
    created_by = relationship("User", foreign_keys=[created_by_id])
    modified_by = relationship("User", foreign_keys=[modified_by_id])

    def __repr__(self) -> str:
        return f"<Loan id={self.id} member_id={self.member_id} amount={self.amount}>"
