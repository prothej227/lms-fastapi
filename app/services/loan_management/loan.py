from typing import List, Optional
from app.repositories.loan_management.loan_type import LoanTypeRepository
from app.models.loan_type import LoanType
from app.schemas.loan_management import LoanTypeCreate, LoanTypeUpdate

async def create_loan_type(
    loan_type_create_data: LoanTypeCreate, 
    db: LoanTypeRepository
) -> LoanType:
    loan_type_repo = LoanTypeRepository(db)
    loan_type = LoanType(**loan_type_create_data.model_dump())
    return await loan_type_repo.create_loan_type(loan_type)

async def update_loan_type(
    loan_type_update_data: LoanTypeUpdate,
    db: LoanTypeRepository
) -> LoanType:
    loan_type_repo = LoanTypeRepository(db)
    loan_type = LoanType(**loan_type_update_data.model_dump())
    return await loan_type_repo.update_loan_type(loan_type)

async def get_loan_type_by_name(
    name: str, 
    db: LoanTypeRepository
) -> LoanType:
    loan_type_repo = LoanTypeRepository(db)
    return await loan_type_repo.get_loan_type(name)

async def get_all_loan_types(
    db: LoanTypeRepository,
    start_index: int,
    page_size: int
) -> Optional[List[LoanType]]:
    loan_type_repo = LoanTypeRepository(db)
    return await loan_type_repo.get_all_loan_types(start_index, page_size)