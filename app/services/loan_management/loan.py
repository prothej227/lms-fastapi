from typing import List, Optional
from app.repositories.loan_management.loan_type import LoanTypeRepository
from app.models.loan import Loan
from app.schemas.loan_management.loan import LoanCreate, LoanView
from sqlalchemy.ext.asyncio import AsyncSession


async def create_loan(
    loan_create_data: LoanCreate, db: AsyncSession
) -> Loan:
    loan_type_repo = LoanTypeRepository(db)
    loan_type = Loan(**loan_create_data.model_dump())
    return await loan_type_repo.create(loan_type)