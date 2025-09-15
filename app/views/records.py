from fastapi import status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from app.views import APIRouter, Depends, HTTPException
from app.database import get_db
from app.services.auth import get_current_user
from app.schemas.user import UserView
from app.services import records as services
from app.schemas import records as schemas
from typing import List
from app.core.config import get_settings

record_router = APIRouter(prefix="/record", tags=["Master Records"])


@record_router.post(
    "/create/member", response_model=schemas.member.MemberCreateResponseView
)
async def create_member_endpoint(
    member_create_data: schemas.member.MemberCreate,
    current_user: UserView = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> schemas.member.MemberCreateResponseView:

    service = services.member.MemberService(db)
    member_create_data = member_create_data.model_copy(
        update={"created_by_id": current_user.id if current_user else -1}
    )
    try:
        member = await service.create(member_create_data)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Member with the same identifier already exists.",
        )
    if member is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Failed creating member."
        )
    return schemas.member.MemberCreateResponseView(
        message="Member created successfully.", member_id=member.id
    )


@record_router.get(
    "/get-all/member", response_model=schemas.member.MemberResponseWithCount
)
async def get_all_members_endpoint(
    current_user: UserView = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    start_index: int = 0,
    batch_size=get_settings().sqlalchemy_default_batch_size,
    filters: schemas.member.MemberRequestFilters = Depends(),
) -> schemas.member.MemberResponseWithCount:
    service = services.member.MemberService(db)
    try:
        all_members = await service.get_all_denorm_with_count(
            start_index,
            batch_size,
            relationships=["created_by", "modified_by"],
            filters=filters.model_dump(exclude_none=True) if filters else {},
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve members.",
        )
    return schemas.member.MemberResponseWithCount(
        total_count=all_members["total_count"],
        records=[
            schemas.member.MemberView.from_orm_with_names(item)
            for item in all_members["records"]
        ],
    )


@record_router.get(
    "/get-all/beneficiary", response_model=List[schemas.beneficiary.BeneficiaryView]
)
async def get_all_beneficiaries_endpoint(
    member_id: int,
    current_user: UserView = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    start_index: int = 0,
    batch_size=get_settings().sqlalchemy_default_batch_size,
) -> List[schemas.beneficiary.BeneficiaryView]:
    service = services.member.MemberService(db)
    beneficiaries = await service.get_all_beneficiaries(
        start_index, batch_size, member_id
    )
    return [
        schemas.beneficiary.BeneficiaryView.model_validate(item)
        for item in beneficiaries
    ]


@record_router.get("/get/member/{member_id}", response_model=schemas.member.MemberView)
async def get_member_by_id_endpoint(
    member_id: int,
    current_user: UserView = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> schemas.member.MemberView:
    service = services.member.MemberService(db)
    member = await service.get_by_id(
        member_id, relationships=["created_by", "modified_by"]
    )
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Member with ID {member_id} not found.",
        )
    return schemas.member.MemberView.from_orm_with_names(member)


@record_router.post(
    "/create/loan-activity", response_model=schemas.loan_activity.LoanActivityRead
)
async def create_loan_activity_endpoint(
    loan_activity_data: schemas.loan_activity.LoanActivityCreate,
    current_user: UserView = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> schemas.loan_activity.LoanActivityRead:
    service = services.loan_activity.LoanActivityService(db)
    loan_activity = await service.create(loan_activity_data)
    if not loan_activity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to create loan activity.",
        )
    return schemas.loan_activity.LoanActivityRead.model_validate(loan_activity)


@record_router.get(
    "/get-all/loan-activity",
    response_model=schemas.loan_activity.LoanActivityResponseWithCount,
)
async def get_all_loan_activity_endpoint(
    current_user: UserView = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    start_index: int = 0,
    batch_size=get_settings().sqlalchemy_default_batch_size,
) -> schemas.loan_activity.LoanActivityResponseWithCount:

    service = services.loan_activity.LoanActivityService(db)
    loan_activities = await service.get_all_denorm_with_count(start_index, batch_size)

    return schemas.loan_activity.LoanActivityResponseWithCount(
        total_count=loan_activities["total_count"],
        records=[
            schemas.loan_activity.LoanActivityRead.model_validate(record)
            for record in loan_activities["records"]
        ],
    )


# @record_router.post(
#     "/post-payment"
# )
