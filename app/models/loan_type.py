from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base


class LoanType(Base):
    __tablename__ = "loan_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(
        String(50), nullable=False, unique=True
    )  # e.g., 'Personal', 'Business', 'Housing'
    description = Column(String(255), nullable=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    modified_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )
    modified_at = Column(
        DateTime, onupdate=lambda: datetime.now(timezone.utc), nullable=True
    )

    loans = relationship("Loan", back_populates="loan_type")

    def __repr__(self):
        return f"<LoanType {self.name}>"
