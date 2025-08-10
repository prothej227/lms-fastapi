from app.services.crud import CrudService
from app.schemas import loan_management as schemas
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import LoanApplication
from app.repositories.loan_management.loan_application import LoanApplicationRepository


class LoanApplicationService(
    CrudService[
        LoanApplication,
        schemas.loan_application.LoanApplicationCreate,
        schemas.loan_type.LoanTypeUpdate,
    ]
):
    def __init__(self, db: AsyncSession):
        super().__init__(LoanApplication, LoanApplicationRepository, db)
