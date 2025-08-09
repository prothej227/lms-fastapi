from sqlalchemy import Integer, String, Date, ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship, mapped_column, Mapped
from datetime import date


class Beneficiary(Base):
    __tablename__ = "beneficiaries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    member_id: Mapped[int] = mapped_column(Integer, ForeignKey("members.id"))
    full_name: Mapped[int] = mapped_column(String(255))
    relationship_type: Mapped[str] = mapped_column(String(255))
    dob: Mapped[date] = mapped_column(Date)
    occupation: Mapped[str] = mapped_column(String(255))
    employer: Mapped[str] = mapped_column(String(255))

    member = relationship("Member", back_populates="beneficiaries")
