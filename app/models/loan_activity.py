from sqlalchemy import Column, Integer, Numeric, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base
from app.models import Loan

class LoanActivity(Base):
    __tablename__ = "loan_activities"

    id = Column(Integer, primary_key=True, index=True)
    loan_id = Column(Integer, ForeignKey("loans.id"), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    activity_type = Column(
        String(50), nullable=False
    )  # e.g., 'Payment', 'Penalty', etc.
    description = Column(String(255), nullable=True)
    balance_after = Column(Numeric(10, 2), nullable=False)
    created_at = Column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )
    loan = relationship("Loan", back_populates="loan_activities")

    def __repr__(self):
        return f"<LoanActivity {self.activity_type} on Loan {self.loan_id}>"
