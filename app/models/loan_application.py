from sqlalchemy import Column, Integer, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base
from app.models.loan import LoanStatus


class LoanApplication(Base):
    __tablename__ = "loan_applications"

    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey("members.id"), nullable=False)
    loan_type_id = Column(Integer, ForeignKey("loan_types.id"), nullable=False)
    amount_requested = Column(Numeric(10, 2), nullable=False)
    application_date = Column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )
    status = Column(Integer, nullable=False, default=LoanStatus.FOR_APPROVAL)
    loan_id = Column(Integer, ForeignKey("loans.id"), nullable=True)

    member = relationship("Member")
    loan_type = relationship("LoanType")
    loan = relationship("Loan")

    def __repr__(self):
        return f"<LoanApplication {self.id} - Member {self.member_id}>"
