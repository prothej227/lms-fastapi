from app.services.crud import CrudService
from app.schemas import loan_management as schemas
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import LoanType
from app.repositories.loan_management.loan_type import LoanTypeRepository


class LoanTypeService(
    CrudService[
        LoanType, schemas.loan_type.LoanTypeCreate, schemas.loan_type.LoanTypeUpdate
    ]
):
    def __init__(self, db: AsyncSession):
        super().__init__(LoanType, LoanTypeRepository, db)
