from app.services.crud import CrudService
from app.schemas import records as schemas
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Member, Beneficiary
from app.repositories.records.member import MemberRepository
from typing import List
from datetime import date


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

        beneficiaries = [
            Beneficiary(**b_data, member=member)  # or member_id=member.id in repo
            for b_data in beneficiaries_data or []
        ]
        member.beneficiaries = beneficiaries

        return await self.repo.create(member)

    async def is_member(
        self,
        member_id: int | str,
        member_first_name: str,
        member_last_name: str,
        member_dob: date,
    ) -> bool:
        return await self.repo.exists(
            pk_config={"fieldName": "member_id", "fieldValue": member_id},
            other_field_queries={
                "first_name": member_first_name,
                "last_name": member_last_name,
                "dob": member_dob,
            },
        )

    async def get_all_beneficiaries(
        self, start_index: int, batch_size: int, member_id: int
    ) -> List[Beneficiary]:
        return await self.repo.get_all_beneficiaries(start_index, batch_size, member_id)
