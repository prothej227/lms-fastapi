from sqlalchemy import Integer, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped
from datetime import datetime, timezone
from app.database import Base
from app.models.loan import LoanStatus
from decimal import Decimal
from app.core.config import get_settings
from zoneinfo import ZoneInfo


class LoanApplication(Base):
    __tablename__ = "loan_applications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    member_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("members.id"), nullable=False
    )
    loan_type_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("loan_types.id"), nullable=False
    )
    amount_requested: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    application_date: Mapped[DateTime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(ZoneInfo(get_settings().timezone)),
        nullable=False,
    )
    status: Mapped[int] = mapped_column(
        Integer, nullable=False, default=LoanStatus.FOR_APPROVAL
    )
    loan_id: Mapped[int] = mapped_column(Integer, ForeignKey("loans.id"), nullable=True)

    member = relationship("Member")
    loan_type = relationship("LoanType")
    loan = relationship("Loan")

    def __repr__(self):
        return f"<LoanApplication {self.id} - Member {self.member_id}>"
