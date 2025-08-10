from app.services.crud import CrudService
from app.schemas import records as schemas
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Member, Beneficiary
from app.repositories.records.member import MemberRepository
from typing import List


class MemberService(
    CrudService[Member, schemas.member.MemberCreate, schemas.member.MemberUpdate]
):
    def __init__(self, db: AsyncSession):
        super().__init__(Member, MemberRepository, db)
        self.repo: MemberRepository = self.repo

    async def create(self, create_data: schemas.member.MemberCreate) -> Member:
        data = create_data.model_dump()
        beneficiaries_data = data.pop("beneficiaries", [])

        member = Member(**data)

        for b_data in beneficiaries_data:
            beneficiary = Beneficiary(**b_data)
            member.beneficiaries.append(beneficiary)

        return await self.repo.create(member)

    async def get_all_beneficiaries(
        self, start_index: int, batch_size: int, member_id: int
    ) -> List[Beneficiary]:
        return await self.repo.get_all_beneficiaries(start_index, batch_size, member_id)
