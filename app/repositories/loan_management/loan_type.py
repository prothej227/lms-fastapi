from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.loan_type import LoanType
from typing import List, Optional

class LoanTypeRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    # Create 
    async def create_loan_type(self, loan_type: LoanType) -> LoanType:
        self.db.add(loan_type)
        await self.db.commit()
        await self.db.refresh(loan_type)
        return loan_type
    
    # Read
    async def get_loan_type(self, name: str) -> Optional[LoanType]:
        _result = await self.db.execute(
            select(LoanType).filter(LoanType.name==name)
        )
        return _result.scalars().first()

    async def get_loan_type_by_id(self, id: int) -> Optional[LoanType]:
        _result = await self.db.execute(
            select(LoanType).filter(LoanType.id==id)
        )
        return _result.scalars().first()

    async def get_all_loan_types(self) -> List[LoanType]:
        _result = await self.db.execute(
            select(LoanType)
        )
        return list(_result.scalars().all())

    # Update
    async def update_loan_type(self, loan_type: LoanType) -> LoanType:
        merged = await self.db.merge(loan_type)
        await self.db.commit()
        await self.db.refresh(merged)
        return merged