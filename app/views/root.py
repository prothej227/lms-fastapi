from app.views import APIRouter,status
router = APIRouter(tags=["Root"])

@router.get("/health_check", status_code=status.HTTP_200_OK)
async def health_check():
    return {"status": "healthy"}