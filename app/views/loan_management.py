from fastapi import status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from app.views import APIRouter, Depends, HTTPException
from app.database import get_db
from app.services.auth import get_current_user
from app.schemas.user import UserView
from typing import List, Dict, Optional, Any
from app.core.config import get_settings
from app.services import loan_management as services
from app.schemas import loan_management as schemas
from app.services import records as record_services

loan_router = APIRouter(prefix="/loan", tags=["Loan Management"])


@loan_router.post(
    "/create/loan-type", response_model=schemas.loan_type.LoanTypeResponse
)
async def create_loan_type_endpoint(
    loan_type_data: schemas.loan_type.LoanTypeBase,
    current_user: UserView = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> schemas.loan_type.LoanTypeResponse:

    service = services.LoanTypeService(db)

    loan_type_create = schemas.loan_type.LoanTypeCreate(
        **loan_type_data.model_dump(),
        created_by_id=current_user.id if current_user.id else -1,
    )

    try:
        loan_type = await service.create(loan_type_create)
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
    "/get-all/loan-type", response_model=schemas.loan_type.LoanTypeResponseWithCount
)
async def get_all_loan_types_endpoint(
    start_index: int = 0,
    batch_size: int = get_settings().sqlalchemy_default_batch_size,
    _current_user: UserView = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    filters: schemas.loan_type.LoanTypeRequestFilters = Depends(),
) -> schemas.loan_type.LoanTypeResponseWithCount:

    service = services.LoanTypeService(db)

    try:
        all_loan_types = await service.get_all_denorm_with_count(
            start_index,
            batch_size,
            relationships=["created_by", "modified_by"],
            filters=filters.model_dump(exclude_none=True),
        )
    except Exception as e:
        raise HTTPException(detail=str(e), status_code=status.HTTP_404_NOT_FOUND)
    if all_loan_types is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to fetch loan type"
        )
    return schemas.loan_type.LoanTypeResponseWithCount(
        total_count=all_loan_types["total_count"],
        records=[
            schemas.loan_type.LoanTypeResponse.from_orm_with_names(lt)
            for lt in all_loan_types["records"]
        ],
    )


@loan_router.post("/create/loan", response_model=schemas.loan.LoanView)
async def create_loan_endpoint(
    loan_data: schemas.loan.LoanBase,
    _current_user: UserView = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> schemas.loan.LoanView:

    service = services.LoanService(db)
    loan_data_create = schemas.loan.LoanCreate(
        **loan_data.model_dump(),
        created_by_id=_current_user.id if _current_user.id else -1,
        modified_by_id=_current_user.id if _current_user.id else -1,
    )

    try:
        loan = await service.create(loan_data_create)
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
    return schemas.loan.LoanView.model_validate(
        {
            **loan.__dict__,
            "created_by_name": _current_user.full_name,
            "modified_by_name": None,
            "loan_type_name": None,
        }
    )


@loan_router.get("/get-all/loan", response_model=schemas.loan.LoanResponseWithCount)
async def get_all_loans_endpoint(
    start_index: int = 0,
    batch_size: int = get_settings().sqlalchemy_default_batch_size,
    _current_user: UserView = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    filters: schemas.loan.LoanRequestFilters = Depends(),
) -> schemas.loan.LoanResponseWithCount:

    service = services.LoanService(db)

    try:
        all_loans = await service.get_all_denorm_with_count(
            start_index,
            batch_size,
            relationships=["created_by", "modified_by", "loan_type"],
            filters=filters.model_dump(exclude_none=True),
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
    return schemas.loan.LoanResponseWithCount(
        total_count=all_loans["total_count"],
        records=[
            schemas.loan.LoanView.from_orm_with_names(loan)
            for loan in all_loans["records"]
        ],
    )


@loan_router.post(
    "/create/loan-application",
    response_model=schemas.loan_application.LoanApplicationView,
)
async def create_loan_application_endpoint(
    loan_application_form: schemas.loan_application.LoanApplicationCreateForm,
    db: AsyncSession = Depends(get_db),
):
    service = services.LoanApplicationService(db)
    member_service = record_services.member.MemberService(db)

    is_member = await member_service.is_member(
        member_id=loan_application_form.member_id,
        member_first_name=loan_application_form.member_first_name,
        member_last_name=loan_application_form.member_last_name,
        member_dob=loan_application_form.member_dob,
    )

    if not is_member:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Given credentials don't exist in our records.",
        )

    try:
        loan_application = await service.create(
            schemas.loan_application.LoanApplicationCreate(
                member_id=loan_application_form.member_id,
                amount_requested=loan_application_form.amount_requested,
                application_date=loan_application_form.application_date,
                loan_type_id=loan_application_form.loan_type_id,
            )
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create loan application. Server error occurred: {str(e)}",
        )

    if loan_application is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No loan application created. Request error occured.",
        )
    return schemas.loan_application.LoanApplicationView.model_validate(loan_application)


@loan_router.get(
    "/get-all/loan-application",
    response_model=schemas.loan_application.LoanApplicationResponseWithCount,
)
async def get_all_loan_applications_endpoint(
    start_index: int = 0,
    batch_size: int = get_settings().sqlalchemy_default_batch_size,
    _current_user: UserView = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    filters: schemas.loan_application.LoanApplicationRequestFilters = Depends(),
) -> schemas.loan_application.LoanApplicationResponseWithCount:

    service = services.LoanApplicationService(db)

    try:
        all_loans = await service.get_all_denorm_with_count(
            start_index,
            batch_size,
            relationships=["member", "loan_type"],
            filters=filters.model_dump(exclude_none=True),
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
    return schemas.loan_application.LoanApplicationResponseWithCount(
        total_count=all_loans["total_count"],
        records=[
            schemas.loan_application.LoanApplicationView.from_orm_with_names(loan)
            for loan in all_loans["records"]
        ],
    )


@loan_router.patch(
    "/update/loan-application/{loan_application_id}",
    response_model=schemas.loan_application.LoanApplicationView,
)
async def update_loan_application_endpoint(
    loan_application_id: int,
    loan_application_form: schemas.loan_application.LoanApplicationUpdate,
    db: AsyncSession = Depends(get_db),
):
    service = services.LoanApplicationService(db)

    try:
        loan_application = await service.update(
            loan_application_id, loan_application_form
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update loan application. Server error occurred: {str(e)}",
        )

    if loan_application is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No loan application updated. Request error occurred.",
        )
    return schemas.loan_application.LoanApplicationView.model_validate(loan_application)


@loan_router.get("/get/schedule/{loan_id}", response_model=List[dict])
async def get_loan_amortization_schedule(
    loan_id: int,
    db: AsyncSession = Depends(get_db),
    _current_user: UserView = Depends(get_current_user),
) -> List[dict]:

    service = services.LoanService(db)

    try:
        schedule = await service.create_amortization_schedule(loan_id)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create amortization schedule. Server error occurred: {str(e)}",
        )

    if schedule is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Loan schedule is not generated. Request error occurred.",
        )
    return schedule
