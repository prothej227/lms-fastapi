from sqlalchemy import Integer, String, Date, ForeignKey, DateTime
from sqlalchemy.orm import relationship, mapped_column, Mapped
from app.database import Base
from datetime import datetime, timezone, date


class Member(Base):
    __tablename__ = "members"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(String(255))
    middle_name: Mapped[str] = mapped_column(String(255))
    last_name: Mapped[str] = mapped_column(String(255))
    birth_address: Mapped[str] = mapped_column(String(255))
    dob: Mapped[date] = mapped_column(Date)
    nationality: Mapped[str] = mapped_column(String(255))
    religion: Mapped[str] = mapped_column(String(255))
    sex: Mapped[str] = mapped_column(String(6))
    civil_status: Mapped[str] = mapped_column(String(50))
    current_address: Mapped[str] = mapped_column(String(255))
    permanent_address: Mapped[str] = mapped_column(String(255))
    contact_number: Mapped[str] = mapped_column(String(20))
    zip_code: Mapped[str] = mapped_column(String(10))
    tin_number: Mapped[str] = mapped_column(String(40))
    id_type1: Mapped[str] = mapped_column(String(25))
    id_type2: Mapped[str] = mapped_column(String(25))
    id_number1: Mapped[str] = mapped_column(String(30))
    id_number2: Mapped[str] = mapped_column(String(30))
    basic_education: Mapped[str] = mapped_column(String(255))
    vocational_degree: Mapped[str] = mapped_column(String(255))
    college_degree: Mapped[str] = mapped_column(String(255))
    pos_grad_degree: Mapped[str] = mapped_column(String(255))
    occupation: Mapped[str] = mapped_column(String(10))
    created_by_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )
    modified_by_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )
    modified_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )

    beneficiaries = relationship("Beneficiary", back_populates="member")
    loans = relationship("Loan", back_populates="member")
    created_by = relationship("User", foreign_keys=[created_by_id])
    modified_by = relationship("User", foreign_keys=[modified_by_id])
