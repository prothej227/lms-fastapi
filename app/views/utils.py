from app.core import enums
from typing import List, Union, Dict
from fastapi import HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.views import APIRouter
from app import models
from app.database import get_db
from app.core.type_dict import UtilFilterQueryMap
from app.services import loan_management as lm_services
from async_lru import alru_cache

utils_router = APIRouter(prefix="/utils", tags=["Utilities"])


@utils_router.get("/get-ref-values", status_code=status.HTTP_200_OK)
async def get_reference_values(category: str) -> List[Dict[str, Union[str, int]]]:
    enum_class = enums.REF_ENUMS.get(category.lower())
    if not enum_class:
        raise HTTPException(status_code=404, detail="Unknown reference category")
    return [
        {
            "label": choice.name.replace(
                "_", "-" if choice.name.upper() in enums.HYPEN_LABELS else " "
            ).title(),
            "value": choice.value,
        }
        for choice in enum_class
    ]


@utils_router.get("/get-all-ref-values", status_code=status.HTTP_200_OK)
async def get_all_reference_values() -> Dict[str, List[Dict[str, Union[str, int]]]]:
    """Return all reference values for enums in REF_ENUMS."""

    def format_label(name: str) -> str:
        """Convert enum member name into human-friendly label."""
        separator = "-" if name.upper() in enums.HYPEN_LABELS else " "
        return name.replace("_", separator).title()

    return {
        category: [
            {"label": format_label(choice.name), "value": choice.value}
            for choice in enum_class
        ]
        for category, enum_class in enums.REF_ENUMS.items()
    }


@utils_router.get("/fetch-filters", status_code=status.HTTP_200_OK)
@alru_cache(maxsize=128)
async def get_filter_map(
    record_type: str, db: AsyncSession = Depends(get_db)
) -> List[Dict]:

    query_maps: Dict[str, UtilFilterQueryMap] = {
        "loan_type": {
            "model": models.LoanType,
            "service": lm_services.LoanTypeService(db),
            "field_names": ["name", "id"],
        },
        "loan_activity": {
            "model": models.LoanActivity,
            "service": None,
            "field_names": [],
        },
    }

    config = query_maps.get(record_type)
    if not config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Filter configuration for '{record_type}' not found.",
        )

    service = config["service"]

    if not service:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail=f"Service for '{record_type}' is not implemented.",
        )

    return await service.get_all_denorm(
        start_index=0, batch_size=5000, field_names=config["field_names"]
    )
