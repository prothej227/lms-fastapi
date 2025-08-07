from typing import List, Optional
from app.repositories.loan_management.loan_type import LoanTypeRepository
from app.models.loan_type import LoanType
from app.schemas.loan_management import LoanTypeCreate, LoanTypeUpdate
from sqlalchemy.ext.asyncio import AsyncSession


async def create_loan_type(
    loan_type_create_data: LoanTypeCreate, db: AsyncSession
) -> LoanType:
    loan_type_repo = LoanTypeRepository(db)
    loan_type = LoanType(**loan_type_create_data.model_dump())
    return await loan_type_repo.create(loan_type)


async def update_loan_type(
    loan_type_update_data: LoanTypeUpdate, db: AsyncSession
) -> LoanType:
    loan_type_repo = LoanTypeRepository(db)
    loan_type = LoanType(**loan_type_update_data.model_dump())
    return await loan_type_repo.update(loan_type)


async def get_loan_type_by_name(name: str, db: AsyncSession) -> LoanType:
    loan_type_repo = LoanTypeRepository(db)
    return await loan_type_repo.get_by_field(field="name", value=name)


async def get_all_loan_types(
    db: AsyncSession, start_index: int, page_size: int
) -> Optional[List[LoanType]]:
    loan_type_repo = LoanTypeRepository(db)
    return await loan_type_repo.get_all_denorm(start_index, page_size)
