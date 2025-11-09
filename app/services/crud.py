from typing import Type, Generic, List, Optional, Any, Union, Dict, TypedDict
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.abstract import AbstractAsyncRepository
from app.core.types import RecordType, CreateSchemaType, UpdateSchemaType


class RecordResponseWithCount(TypedDict):
    total_count: int
    records: Any


class CrudService(Generic[RecordType, CreateSchemaType, UpdateSchemaType]):
    """
    Base CRUD Service for LMS RecordType

    Args:
        model (RecordType): The SQLAchemy DB Model based from declarative base.
        repository_class (AbstractAsyncRepository): The repository class of the DB Model
        db (AsyncSession): The DB session instance

    Return:
        None
    """

    def __init__(
        self,
        model: Type[RecordType],
        repository_class: Type[AbstractAsyncRepository],
        db: AsyncSession,
    ):
        self.model = model
        self.repo = repository_class(db)

    async def create(self, create_data: CreateSchemaType) -> RecordType:
        obj = self.model(**create_data.model_dump())
        return await self.repo.create(obj)

    async def update(self, id: int, update_data: UpdateSchemaType) -> RecordType:
        return await self.repo.update(id, update_data.model_dump(exclude_unset=True))

    async def get_by_field(self, field: str, value: Any) -> Optional[RecordType]:
        return await self.repo.get_by_field(field, value)

    async def get_by_id(
        self, id: int, relationships: Optional[List[str]] = None
    ) -> Optional[RecordType]:
        return await self.repo.get_by_id(id, relationships=relationships)

    async def count_all(self) -> int:
        return await self.repo.count_all()

    async def count_all_filtered(self, filters: Dict[str, Any]) -> int:
        return await self.repo.count_all(filters=filters)

    async def get_all_denorm_with_count(
        self,
        start_index: int,
        batch_size: int,
        field_names: Optional[List[str]] = None,
        relationships: Optional[List[str]] = None,
        filters: Optional[Dict[str, Any]] = None,
    ) -> RecordResponseWithCount:
        records = await self.repo.get_all_denorm(
            start_index, batch_size, field_names, relationships, filters
        )
        total_count = await self.repo.count_all(filters=filters)
        return {"total_count": total_count, "records": records}

    async def get_all_denorm(
        self,
        start_index: int,
        batch_size: int,
        field_names: Optional[List[str]] = None,
        relationships: Optional[List[str]] = None,
        filters: Optional[Dict[str, Any]] = None,
    ) -> Union[List[Dict[str, Any]], List[RecordType]]:
        return await self.repo.get_all_denorm(
            start_index, batch_size, field_names, relationships, filters
        )

    async def get_all(self, start_index: int, batch_size: int) -> List[RecordType]:
        return await self.repo.get_all(start_index, batch_size)
