from pydantic import BaseModel
from typing import Dict, Any, List


class DashboardSummaryResponse(BaseModel):
    loan_count: int
    payment_count: int
    member_count: int
    loan_application_count: int
    current_month_count: int
    area_chart_data: Dict[str, Any]
    daily_loan_activities: List[Dict]
