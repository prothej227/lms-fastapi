from sqlalchemy.ext.asyncio import AsyncSession
from app.models.loan import Loan
from app.models.loan_type import LoanType
from app.models.loan_activity import LoanActivity
from app.models.loan_application import LoanApplication
from sqlalchemy.future import select
from typing import List, Optional

class LoanRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_loan(self, loan: Loan) -> Loan:
        self.db.add(loan)
        await self.db.commit()
        await self.db.refresh(loan)
        return loan

    async def get_loan_by_id(self, id: int) -> Optional[Loan]:
        _result = await self.db.execute(
            select(Loan).filter(Loan.id==id)
        )
        return _result.scalar_one_or_none()
    
    async def get_all_loans(self) -> List[Loan]:
        _result = await self.db.execute(
            select(Loan)
        )
        return list(_result.scalars().all())

    async def update_loan(self, loan: Loan) -> Optional[Loan]:
        merged = await self.db.merge(loan)
        await self.db.commit()
        await self.db.refresh(merged)
        return merged

    async def delete_loan(self, id: int) -> bool:
        try: 
            loan: Loan = await self.get_loan(id)
            if loan:
                await self.db.delete(loan)
                await self.db.commit()
                return True
            return False
        except Exception:
            await self.db.rollback()
        return False
    