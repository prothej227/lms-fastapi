from app.services.crud import CrudService
from app.schemas import loan_management as schemas
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Loan
from app.repositories.loan_management.loan import LoanRepository


class LoanService(CrudService[Loan, schemas.loan.LoanCreate, schemas.loan.LoanUpdate]):
    def __init__(self, db: AsyncSession):
        super().__init__(Loan, LoanRepository, db)
