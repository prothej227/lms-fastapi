from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, Dict
import asyncio

from app.services.loan_management import LoanApplicationService, LoanService
from app.services.records import MemberService, LoanActivityService


class DashboardService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.loan_service = LoanService(db)
        self.loan_activity_service = LoanActivityService(db)
        self.member_service = MemberService(db)
        self.loan_application_service = LoanApplicationService(db)

    async def get_loan_count(self) -> int:
        return await self.loan_service.count_all()

    async def get_payment_count(self) -> int:
        return await self.loan_activity_service.count_all()

    async def get_member_count(self) -> int:
        return await self.member_service.count_all()

    async def get_loan_application_count(self) -> int:
        return await self.loan_application_service.count_all()

    async def get_summary(self) -> Dict[str, int]:
        loan_coro = self.get_loan_count()
        payment_coro = self.get_payment_count()
        member_coro = self.get_member_count()
        application_coro = self.get_loan_application_count()

        loan_count, payment_count, member_count, application_count = (
            await asyncio.gather(loan_coro, payment_coro, member_coro, application_coro)
        )

        return {
            "loan_count": loan_count,
            "payment_count": payment_count,
            "member_count": member_count,
            "loan_application_count": application_count,
        }
