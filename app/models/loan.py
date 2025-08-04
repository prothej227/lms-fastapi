from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, Date
from sqlalchemy.orm import relationship
from datetime import date
from app.database import Base


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

    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey("members.id"), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    interest_rate = Column(Numeric(4, 2), nullable=False)
    start_date = Column(Date, nullable=False, default=date.today)
    end_date = Column(Date, nullable=False)
    loan_type_id = Column(Integer, ForeignKey("loan_types.id"), nullable=False)
    status = Column(Integer, nullable=False, default=LoanStatus.FOR_APPROVAL)
    outstanding_balance = Column(Numeric(10, 2), nullable=False)
    total_interest = Column(Numeric(10, 2), nullable=False, default=0.00)
    total_paid = Column(Numeric(10, 2), nullable=False, default=0.00)
    description = Column(String(255), nullable=True)

    # Relationships (define related models separately)
    activities = relationship("LoanActivity", back_populates="loan")
    loan_type = relationship("LoanType", back_populates="loans")
    member = relationship("Member", back_populates="loans")
