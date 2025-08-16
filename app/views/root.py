from app.views import APIRouter, status


root_router = APIRouter(tags=["Root"])


@root_router.get("/health_check", status_code=status.HTTP_200_OK)
async def health_check():
    return {"status": "healthy"}
