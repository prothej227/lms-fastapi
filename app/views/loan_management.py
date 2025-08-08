from fastapi import status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from app.views import APIRouter, Depends, HTTPException
from app.database import get_db
from app.services.auth import get_current_user
from app.schemas.user import UserView
from typing import List
from app.core.config import get_settings
from app.services import loan_management as services
from app.schemas import loan_management as schemas

loan_router = APIRouter(prefix="/loan", tags=["Loan Management"])


@loan_router.post(
    "/create/loan-type", response_model=schemas.loan_type.LoanTypeResponse
)
async def create_loan_type_endpoint(
    loan_type_data: schemas.loan_type.LoanTypeCreate,
    current_user: UserView = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> schemas.loan_type.LoanTypeResponse:
    loan_type_data.created_by_id = current_user.id if current_user.id else -1
    try:
        loan_type = await services.loan_type.create_loan_type(loan_type_data, db)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Loan type with similar data already exists.",
        )

    if not loan_type:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to create loan type"
        )

    return schemas.loan_type.LoanTypeResponse.model_validate(
        {
            **loan_type.__dict__,
            "created_by_name": current_user.full_name,
            "modified_by_name": None,
        }
    )


@loan_router.get(
    "/get-all/loan-type", response_model=List[schemas.loan_type.LoanTypeResponse]
)
async def get_all_loan_types_endpoint(
    start_index: int = 0,
    batch_size: int = get_settings().sqlalchemy_default_batch_size,
    _current_user: UserView = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> List[schemas.loan_type.LoanTypeResponse]:
    try:
        all_loan_types = await services.loan_type.get_all_loan_types(
            db, start_index, batch_size
        )
    except Exception as e:
        raise HTTPException(detail=str(e), status_code=status.HTTP_404_NOT_FOUND)
    if all_loan_types is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to fetch loan type"
        )
    return [
        schemas.loan_type.LoanTypeResponse.from_orm_with_names(lt)
        for lt in all_loan_types
    ]


@loan_router.get("/create/loan", response_model=dict)
def create_loan_endpoint() -> dict:
    return {
        "detail": "Soon!"
    }
