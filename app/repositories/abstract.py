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
        self, start_index: int = 0, batch_size: int = 5000
    ) -> List[RecordType]:
        result = await self.db.execute(
            select(self.model).offset(start_index).limit(batch_size)
        )
        return list(result.scalars().all())
    
    async def get_all_denorm(self, start_index: int, page_size: int) -> List[RecordType]:
        result = await self.db.execute(
            select(self.model)
            .options(
                joinedload(self.model.created_by),
                joinedload(self.model.modified_by),
            )
            .offset(start_index)
            .limit(page_size)
        )
        return result.scalars().all()
    
    async def update(self, obj: RecordType) -> RecordType:
        merged = await self.db.merge(obj)
        await self.db.commit()
        await self.db.refresh(merged)
        return merged
