from app.repositories.abstract import AbstractAsyncRepository
from app.models import LoanActivity
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Type


class LoanActivityRepository(AbstractAsyncRepository[LoanActivity]):

    def __init__(self, db: AsyncSession):
        super().__init__(db)

    @property
    def model(self) -> Type[LoanActivity]:
        return LoanActivity
