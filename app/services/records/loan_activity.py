from app.services.crud import CrudService
from app.schemas import records as schemas
from app.models import LoanActivity
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.records.loan_activity import LoanActivityRepository


class LoanActivityService(
    CrudService[
        LoanActivity,
        schemas.loan_activity.LoanActivityCreate,
        schemas.loan_activity.LoanActivityUpdate,
    ]
):
    def __init__(self, db: AsyncSession):
        super().__init__(LoanActivity, LoanActivityRepository, db)
        self.repo: LoanActivityRepository = self.repo
