from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, List, Any
from sqlalchemy import select, func
from app.models import Loan, LoanActivity, Member, LoanApplication
from app.core.enums import LoanActivityStatus, LoanActivityType
from datetime import datetime
import calendar
from app.models.dashboard import DashboardSummaryResponse


class DashboardService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_current_month_loan_count(self) -> int:
        current_month = f"{datetime.now().month:02d}"
        stmt = select(
            select(func.count())
            .select_from(Loan)
            .where(func.strftime("%m", Loan.created_at) == current_month)
            .scalar_subquery()
            .label("current_month_loan_count")
        )
        res = await self.db.execute(stmt)
        row = res.one()
        m = row._mapping
        return m["current_month_loan_count"]

    async def get_daily_loan_count_from_month_range(self) -> List[Dict]:
        now = datetime.now()
        current_year, current_month = int(now.year), int(now.month)
        num_days = calendar.monthrange(current_year, current_month)[1]
        year_str = f"{current_year:04d}"
        month_str = f"{current_month:02d}"

        stmt = (
            (
                select(
                    func.strftime("%m-%d-%Y", Loan.created_at).label("loan_date"),
                    func.count().label("loan_count"),
                )
            )
            .where(
                func.strftime("%Y", Loan.created_at == year_str),
                func.strftime("%m", Loan.created_at == month_str),
            )
            .group_by(func.strftime("%Y-%m-%d", Loan.created_at))
            .order_by(func.strftime("%Y-%m-%d", Loan.created_at))
        )

        res = await self.db.execute(stmt)
        rows = {r.loan_date: int(r.loan_count) for r in res.all()}

        days_in_month_list: List[Dict[str, int]] = []

        for day in range(1, num_days + 1):
            key = f"{month_str}-{day:02d}-{year_str}"
            days_in_month_list.append({key: rows.get(key, 0)})
        return days_in_month_list

    async def get_monthly_loan_count_from_year_range(
        self, months: int = 24
    ) -> Dict | List:
        now = datetime.now()
        current_year, current_month = now.year, now.month

        if months <= 0:
            return []

        start_total = current_year * 12 + current_month - (months - 1)
        ym_list: List[str] = []
        for i in range(months):
            t = start_total + i
            year = (t - 1) // 12
            month = (t - 1) % 12 + 1
            ym_list.append(f"{year:04d}-{month:02d}")

        stmt = (
            select(
                func.strftime("%Y-%m", Loan.created_at).label("ym"),
                func.count().label("loan_count"),
            )
            .where(func.strftime("%Y-%m", Loan.created_at).in_(ym_list))
            .group_by(func.strftime("%Y-%m", Loan.created_at))
            .order_by(func.strftime("%Y-%m", Loan.created_at))
        )

        res = await self.db.execute(stmt)
        rows = {r.ym: int(r.loan_count) for r in res.all()}

        labels, values = [], []

        for ym in ym_list:
            y_str, m_str = ym.split("-")
            y, m = int(y_str), int(m_str)
            label = f"{calendar.month_abbr[m]} {y}"
            labels.append(label)
            values.append(f"{rows.get(ym, 0)}")

        return {"label": "Monthly Loan Count", "labels": labels, "values": values}

    async def get_daily_loan_activities_from_month_range(self) -> List[Dict]:
        now = datetime.now()
        current_year, current_month = int(now.year), int(now.month)
        num_days = calendar.monthrange(current_year, current_month)[1]
        year_str = f"{current_year:04d}"
        month_str = f"{current_month:02d}"

        # Just select all loan_activities for the current month year, not the count
        stmt = (
            select(
                LoanActivity.loan_activity_code,
                LoanActivity.activity_type,
                LoanActivity.status,
                func.strftime("%m/%d %H:%M%p", LoanActivity.created_at).label(
                    "created_at"
                ),
            )
        ).where(
            func.strftime("%Y", LoanActivity.created_at) == year_str,
            func.strftime("%m", LoanActivity.created_at) == month_str,
            LoanActivity.activity_type == LoanActivityType.PAYMENT.value,
        )

        res = await self.db.execute(stmt)
        return [dict(row) for row in res.mappings().all()]

    async def get_summary(self) -> DashboardSummaryResponse:
        _loan_count_stmt = (
            select(func.count()).select_from(Loan).scalar_subquery().label("loan_count")
        )
        _payment_count_stmt = (
            select(func.count())
            .select_from(LoanActivity)
            .where(LoanActivity.activity_type == LoanActivityType.PAYMENT.value)
            .scalar_subquery()
            .label("payment_count")
        )
        _member_count_stmt = (
            select(func.count())
            .select_from(Member)
            .scalar_subquery()
            .label("member_count")
        )
        _loan_application_count_stmt = (
            select(func.count())
            .select_from(LoanApplication)
            .scalar_subquery()
            .label("loan_application_count")
        )
        stmt = select(
            _loan_count_stmt,
            _payment_count_stmt,
            _member_count_stmt,
            _loan_application_count_stmt,
        )
        res = await self.db.execute(stmt)
        row = res.one()
        m = row._mapping

        return DashboardSummaryResponse(
            loan_count=m["loan_count"],
            payment_count=m["payment_count"],
            member_count=m["member_count"],
            loan_application_count=m["loan_application_count"],
            current_month_count=await self.get_current_month_loan_count(),
            area_chart_data={
                "monthly_loan_count": await self.get_monthly_loan_count_from_year_range(),
            },
            daily_loan_activities=await self.get_daily_loan_activities_from_month_range(),
        )
