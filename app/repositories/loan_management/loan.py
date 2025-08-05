from sqlalchemy.ext.asyncio import AsyncSession
from app.models.loan import Loan
from app.repositories.abstract import AbstractAsyncRepository

from typing import Type


class LoanTypeRepository(AbstractAsyncRepository[Loan]):

    def __init__(self, db: AsyncSession):
        super().__init__(db)

    @property
    def model(self) -> Type[Loan]:
        return Loan
