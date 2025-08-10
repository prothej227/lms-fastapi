from sqlalchemy.ext.asyncio import AsyncSession
from app.models import LoanApplication
from app.repositories.abstract import AbstractAsyncRepository
from typing import Type


class LoanApplicationRepository(AbstractAsyncRepository[LoanApplication]):

    def __init__(self, db: AsyncSession):
        super().__init__(db)

    @property
    def model(self) -> Type[LoanApplication]:
        return LoanApplication
