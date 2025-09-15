from typing import TypedDict, Optional, List
from app.services.crud import CrudService


class UtilFilterQueryMap(TypedDict):
    model: type
    service: Optional[CrudService]
    field_names: List[str]
