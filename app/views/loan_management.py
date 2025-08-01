from fastapi import status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from app.views import APIRouter, Depends, HTTPException
from app.database import get_db
from app.services.auth import get_current_user
from app.schemas.user import UserView
from app.services.loan_management.loan import (
    create_loan_type,
    update_loan_type,
    get_loan_type_by_name,
    get_all_loan_types
)
from app.schemas.loan_management import (
    LoanTypeCreate,
    LoanTypeUpdate,
    LoanTypeResponse
)

loan_router = APIRouter(prefix="/loan", tags=["Loan Management"])

@loan_router.post("/create/loan-type", response_model=LoanTypeResponse)
async def create_loan_type_endpoint(
    loan_type_data: LoanTypeCreate,
    current_user: UserView = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> LoanTypeResponse:
    loan_type_data.created_by = current_user.id
    try:
        loan_type = await create_loan_type(loan_type_data, db)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Loan type with similar data already exists."
        )
    if not loan_type:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to create loan type"
        )
    return LoanTypeResponse(
        id=loan_type.id,
        name=loan_type.name,
        description=loan_type.description,
        created_by_name=current_user.full_name,
        created_at=loan_type.created_at,
        modified_by_name=None,
        modified_at=None
    )