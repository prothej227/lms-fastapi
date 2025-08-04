from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.loan_type import LoanType
from typing import List, Optional


class LoanTypeRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    # Created
    async def create_loan_type(self, loan_type: LoanType) -> LoanType:
        try:
            self.db.add(loan_type)
            await self.db.commit()
            await self.db.refresh(loan_type)
            return loan_type
        except Exception as e:
            await self.db.rollback()
            raise e

    # Read
    async def get_loan_type(self, name: str) -> Optional[LoanType]:
        result = await self.db.execute(select(LoanType).filter(LoanType.name == name))
        return result.scalar_one_or_none()

    async def get_loan_type_by_id(self, id: int) -> Optional[LoanType]:
        result = await self.db.execute(select(LoanType).filter(LoanType.id == id))
        return result.scalar_one_or_none()

    async def get_all_loan_types(
        self, start_index: int = 1, batch_size: int = 5000
    ) -> List[LoanType]:
        result = await self.db.execute(
            select(LoanType).offset(start_index).limit(batch_size)
        )
        return list(result.scalars().all())

    # Update
    async def update_loan_type(self, loan_type: LoanType) -> LoanType:
        merged = await self.db.merge(loan_type)
        await self.db.commit()
        await self.db.refresh(merged)
        return merged
