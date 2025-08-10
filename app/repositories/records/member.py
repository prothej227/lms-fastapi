from app.repositories.abstract import AbstractAsyncRepository
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Member, Beneficiary
from sqlalchemy.future import select
from typing import List, Type


class MemberRepository(AbstractAsyncRepository[Member]):

    def __init__(self, db: AsyncSession):
        super().__init__(db)

    @property
    def model(self) -> Type[Member]:
        return Member

    async def create(self, obj: Member) -> Member:
        try:
            self.db.add(obj)
            await self.db.flush()

            beneficiaries: List[Beneficiary] = obj.beneficiaries

            for beneficiary in beneficiaries:
                beneficiary.member_id = obj.id
                self.db.add(beneficiary)

            await self.db.commit()
            await self.db.refresh(obj)

            return obj
        except Exception as e:
            await self.db.rollback()
            raise e

    async def get_all_beneficiaries(
        self, start_index: int, batch_size: int, member_id: int
    ) -> List[Beneficiary]:
        result = await self.db.execute(
            select(Beneficiary)
            .filter(Beneficiary.member_id == member_id)
            .offset(start_index)
            .limit(batch_size)
        )
        return list(result.scalars().all())
