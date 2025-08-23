from typing import TypedDict, Optional, List
from app.services.crud import CrudService
from app.core.types import RecordTypeModel


class UtilFilterQueryMap(TypedDict):
    model: type
    service: Optional[CrudService]
    field_names: List[str]
