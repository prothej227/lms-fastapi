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


@record_router.post("/create/member", response_model=schemas.member.MemberView)
async def create_member_endpoint(
    member_create_data: schemas.member.MemberCreate,
    current_user: UserView = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> schemas.member.MemberView:

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
    return schemas.member.MemberView.model_validate(member)


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
