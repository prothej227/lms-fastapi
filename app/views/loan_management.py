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

    service = services.LoanTypeService(db)
    loan_type_data = loan_type_data.model_copy(
        update={"created_by_id": current_user.id if current_user.id else -1}
    )

    try:
        loan_type = await service.create(loan_type_data)
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

    service = services.LoanTypeService(db)

    try:
        all_loan_types = await service.get_all_denorm(
            start_index, batch_size, relationships=["created_by", "modified_by"]
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


@loan_router.post("/create/loan", response_model=schemas.loan.LoanView)
async def create_loan_endpoint(
    loan_data: schemas.loan.LoanCreate,
    _current_user: UserView = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> schemas.loan.LoanView:

    service = services.LoanService(db)
    loan_data = loan_data.model_copy(
        update={"created_by_id": _current_user.id if _current_user.id else -1}
    )

    try:
        loan = await service.create(loan_data)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Loan with similar data already exists.",
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="A server error occured",
        )
    if not loan:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to create loan."
        )
    return schemas.loan.LoanView.model_validate(loan)


@loan_router.get("/get-all/loan", response_model=List[schemas.loan.LoanView])
async def get_all_loans_endpoint(
    start_index: int = 0,
    batch_size: int = get_settings().sqlalchemy_default_batch_size,
    _current_user: UserView = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> List[schemas.loan.LoanView]:

    service = services.LoanService(db)

    try:
        all_loans = await service.get_all_denorm(
            start_index, batch_size, ["created_by", "modified_by", "loan_type"]
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="A server error occured.",
        )

    if all_loans is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to fetch loans."
        )
    return [schemas.loan.LoanView.from_orm_with_names(loan) for loan in all_loans]


@loan_router.post(
    "/create/loan-application",
    response_model=schemas.loan_application.LoanApplicationView,
)
async def create_loan_application_endpoint(
    loan_application_data: schemas.loan_application.LoanApplicationCreate,
    db: AsyncSession = Depends(get_db),
):
    service = services.LoanApplicationService(db)
    try:
        loan_application = await service.create(loan_application_data)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Faield to create loan application. Server error occured",
        )

    if loan_application is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No loan application created. Request error occured.",
        )
    return schemas.loan_application.LoanApplicationView.model_validate(loan_application)


@loan_router.get(
    "/get-all/loan-application",
    response_model=List[schemas.loan_application.LoanApplicationView],
)
async def get_all_loan_applications_endpoint(
    start_index: int = 0,
    batch_size: int = get_settings().sqlalchemy_default_batch_size,
    _current_user: UserView = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> List[schemas.loan_application.LoanApplicationView]:

    service = services.LoanApplicationService(db)

    try:
        all_loans = await service.get_all(start_index, batch_size)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="A server error occured.",
        )

    if all_loans is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to fetch loans."
        )
    return [
        schemas.loan_application.LoanApplicationView.model_validate(loan)
        for loan in all_loans
    ]
