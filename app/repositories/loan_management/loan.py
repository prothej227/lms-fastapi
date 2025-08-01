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
        return _result.scalars().first()
    
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
        

    async def create_loan_type(self, loan_type: LoanType) -> LoanType:
        self.db.add(loan_type)
        await self.db.commit()
        await self.db.refresh(loan_type)
        return loan_type

    async def get_loan_type(self, name: str) -> LoanType:
        return await self.db.query(LoanType).filter(LoanType.name==name).first()

    async def create_loan_activity(self, activity: LoanActivity) -> LoanActivity:
        self.db.add(activity)
        await self.db.commit()
        await self.db.refresh(activity)
        return activity

    async def get_loan_activity(self, activity_id: int) -> LoanActivity:
        return await self.db.query(LoanActivity).filter(LoanActivity.id==activity_id).first()

    async def create_loan_application(self, application: LoanApplication) -> LoanApplication:
        self.db.add(application)
        await self.db.commit()
        await self.db.refresh(application)
        return application

    async def get_loan_application(self, application_id: int) -> LoanApplication:
        return await self.db.query(LoanApplication).filter(LoanApplication.id == application_id).first()