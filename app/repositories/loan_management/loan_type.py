from sqlalchemy.ext.asyncio import AsyncSession
from app.models.loan_type import LoanType
from app.repositories.abstract import AbstractAsyncRepository

from typing import Type


class LoanTypeRepository(AbstractAsyncRepository[LoanType]):

    def __init__(self, db: AsyncSession):
        super().__init__(db)

    @property
    def model(self) -> Type[LoanType]:
        return LoanType
    