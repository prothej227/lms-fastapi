from fastapi import status
from app.views import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.dashboard import DashboardService
from typing import Dict, Any
from app.database import get_db
from app.services.auth import get_current_user
from app.models.dashboard import DashboardSummaryResponse

dashboard_router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@dashboard_router.get("/summary", response_model=DashboardSummaryResponse)
async def get_dashboard_summary(
    _current_user: str = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    dashboard_service = DashboardService(db)
    return await dashboard_service.get_summary()
