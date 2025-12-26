from app.views import APIRouter, status

root_router = APIRouter(tags=["Root"])


@root_router.get("/", status_code=status.HTTP_200_OK, response_model=dict)
async def root():
    return {
        "app_name": "Loan Management System",
        "version": "1.0.0",
        "description": "A system for managing loans",
        "author": "Journel Cabrillos",
    }


@root_router.get("/health_check", status_code=status.HTTP_200_OK, response_model=dict)
async def health_check():
    return {"status": "healthy"}
