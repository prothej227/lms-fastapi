from abc import ABC, abstractmethod
from typing import Generic, Type, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.types import RecordType
from sqlalchemy.orm import joinedload


class AbstractAsyncRepository(ABC, Generic[RecordType]):
    def __init__(self, db: AsyncSession):
        self.db = db

    @property
    @abstractmethod
    def model(self) -> Type[RecordType]:
        """Return the SQLAlchemy model associated with the repository."""
        pass

    async def create(self, obj: RecordType) -> RecordType:
        try:
            self.db.add(obj)
            await self.db.commit()
            await self.db.refresh(obj)
            return obj
        except Exception as e:
            await self.db.rollback()
            raise e

    async def get_by_id(self, id: int) -> Optional[RecordType]:
        result = await self.db.execute(select(self.model).filter(self.model.id == id))
        return result.scalar_one_or_none()

    async def get_by_field(self, field: str, value) -> Optional[RecordType]:
        result = await self.db.execute(
            select(self.model).filter(getattr(self.model, field) == value)
        )
        return result.scalar_one_or_none()

    async def get_all(
        self,
        start_index: int,
        batch_size: int,
    ) -> List[RecordType]:
        result = await self.db.execute(
            select(self.model).offset(start_index).limit(batch_size)
        )
        return list(result.scalars().all())

    async def get_all_denorm(
        self,
        start_index: int,
        batch_size: int,
        relationships: Optional[list[str]] = None,
    ) -> List[RecordType]:
        """Get all denormalized records from the defined relationships

        Args:
            start_index (int): Query starting index. Default: 0
            batch_size (int): The number of data you want to obtain, or simply the page size.
            relationships (List[str]): The relationship name e.g. ['created_by', 'modified_by']
        """
        query = select(self.model)

        if relationships:
            query = query.options(
                *(joinedload(getattr(self.model, rel)) for rel in relationships)
            )

        result = await self.db.execute(query.offset(start_index).limit(batch_size))

        return list(result.scalars().all())

    async def update(self, obj: RecordType) -> RecordType:
        merged = await self.db.merge(obj)
        await self.db.commit()
        await self.db.refresh(merged)
        return merged
