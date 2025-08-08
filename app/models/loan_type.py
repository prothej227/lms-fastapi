from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base
from app.models.user import User


class LoanType(Base):
    __tablename__ = "loan_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, unique=True)
    interest_rate = Column(Numeric(4, 2), nullable=False)
    description = Column(String(255), nullable=True)
    created_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    modified_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )
    modified_at = Column(
        DateTime, onupdate=lambda: datetime.now(timezone.utc), nullable=True
    )

    created_by = relationship("User", foreign_keys=[created_by_id])
    modified_by = relationship("User", foreign_keys=[modified_by_id])

    loans = relationship("Loan", back_populates="loan_type")

    def __repr__(self):
        return f"<LoanType {self.name}>"

    loans = relationship("Loan", back_populates="loan_type")

    def __repr__(self):
        return f"<LoanType {self.name}>"
