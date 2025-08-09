from sqlalchemy import Integer, String, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime, timezone
from app.database import Base
from typing import Optional


class LoanType(Base):
    __tablename__ = "loan_types"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    interest_rate: Mapped[float] = mapped_column(Numeric(4, 2), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(255))
    created_by_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    modified_by_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )
    modified_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime, onupdate=lambda: datetime.now(timezone.utc)
    )

    created_by = relationship("User", foreign_keys=[created_by_id])
    modified_by = relationship("User", foreign_keys=[modified_by_id])
    loans = relationship("Loan", back_populates="loan_type")

    def __repr__(self) -> str:
        return f"<LoanType {self.name}>"
