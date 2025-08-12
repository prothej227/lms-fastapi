from typing import Type, Generic, List, Optional, Any
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.abstract import AbstractAsyncRepository
from app.core.types import RecordType, CreateSchemaType, UpdateSchemaType


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

    async def update(self, update_data: UpdateSchemaType) -> RecordType:
        obj = self.model(**update_data.model_dump())
        return await self.repo.update(obj)

    async def get_by_field(self, field: str, value: Any) -> Optional[RecordType]:
        return await self.repo.get_by_field(field, value)

    async def get_all_denorm(
        self, start_index: int, batch_size: int
    ) -> List[RecordType]:
        return await self.repo.get_all_denorm(start_index, batch_size)

    async def get_all(self, start_index: int, batch_size: int) -> List[RecordType]:
        return await self.repo.get_all(start_index, batch_size)
