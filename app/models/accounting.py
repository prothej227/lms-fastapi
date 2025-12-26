from sqlalchemy import Integer, Numeric, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped
from datetime import datetime
from decimal import Decimal
from zoneinfo import ZoneInfo
from app.database import Base
from app.core.config import get_settings


# -------------------------------
# Chart of Accounts
# -------------------------------
class ChartOfAccount(Base):
    __tablename__ = "chart_of_accounts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    code: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    type: Mapped[str] = mapped_column(
        String(50), nullable=False
    )  # e.g., 'Asset', 'Liability', 'Equity', 'Revenue', 'Expense'

    # relationships
    ledger_lines = relationship("GeneralLedgerLine", back_populates="account")

    def __repr__(self):
        return f"<Account {self.code} - {self.name}>"


# -------------------------------
# General Ledger (Header)
# -------------------------------
class GeneralLedger(Base):
    __tablename__ = "general_ledger"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    reference: Mapped[str] = mapped_column(
        String(50), nullable=True
    )  # e.g., loan_activity_id, external ref
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(ZoneInfo(get_settings().timezone)),
        nullable=False,
    )

    # relationships
    lines = relationship(
        "GeneralLedgerLine", back_populates="ledger", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<GL Entry {self.id} - {self.description}>"


# -------------------------------
# General Ledger Line Items
# -------------------------------
class GeneralLedgerLine(Base):
    __tablename__ = "general_ledger_lines"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    ledger_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("general_ledger.id"), nullable=False
    )
    account_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("chart_of_accounts.id"), nullable=False
    )
    debit: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=Decimal("0.00"))
    credit: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=Decimal("0.00"))

    # relationships
    ledger = relationship("GeneralLedger", back_populates="lines")
    account = relationship("ChartOfAccount", back_populates="ledger_lines")

    def __repr__(self):
        return f"<GL Line {self.id} - Debit {self.debit} Credit {self.credit}>"
