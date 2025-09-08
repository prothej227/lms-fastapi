from abc import ABC, abstractmethod
from dataclasses import fields
from typing import Generic, Type, List, Optional, Union, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.types import RecordType
from sqlalchemy.orm import joinedload
from sqlalchemy import and_, func


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

    async def get_by_id(
        self, id: int, relationships: Optional[List[str]] = None
    ) -> Optional[RecordType]:
        query = select(self.model).filter(self.model.id == id)
        if relationships:
            query = query.options(
                *(joinedload(getattr(self.model, rel)) for rel in relationships)
            )
        result = await self.db.execute(query)
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
        field_names: Optional[List[str]] = None,
        relationships: Optional[List[str]] = None,
        filters: Optional[Dict[str, Any]] = None,
    ) -> Union[List[Dict[str, Any]], List[RecordType]]:
        """
        Get all denormalized records from the defined relationships.

        Args:
            start_index (int): Query starting index. Default: 0
            batch_size (int): The number of data you want to obtain, or simply the page size.
            field_names (List[str], optional): Specific field names to select.
            relationships (List[str], optional): Relationships to join-load.
            filters (Dict[str, Any], optional): Filtering conditions {field: value}.
        """

        if field_names:
            query = select(*(getattr(self.model, field) for field in field_names))
        else:
            query = select(self.model)

        if relationships:
            query = query.options(
                *(joinedload(getattr(self.model, rel)) for rel in relationships)
            )

        if filters:
            conditions = []

            for field, value in filters.items():
                col = getattr(self.model, field, None)
                if col is not None and value is not None:
                    if isinstance(value, str):
                        conditions.append(col.ilike(f"%{value}%"))
                    else:
                        conditions.append(col == value)

            if conditions:
                query = query.where(and_(*conditions))

        query = query.offset(start_index).limit(batch_size)

        result = await self.db.execute(query)

        if field_names:
            rows = result.all()
            return [dict(zip(field_names, row)) for row in rows]
        else:

            return list(result.scalars().all())

    async def update(self, id: int, update_data: dict) -> RecordType:
        if id is None or update_data is None:
            raise ValueError("Invalid id or object.")

        existing = await self.get_by_id(id)
        if not existing:
            raise ValueError(f"Record with id {id} does not exist.")

        for key, value in update_data.items():
            setattr(existing, key, value)

        await self.db.commit()
        await self.db.refresh(existing)
        return existing

    async def count_all(self, filters: Optional[Dict[str, Any]] = None) -> int:
        query = select(func.count()).select_from(self.model)

        if filters:
            conditions = []
            for field, value in filters.items():
                col = getattr(self.model, field, None)
                if col is not None and value is not None:
                    if isinstance(value, str):
                        # case-insensitive partial match
                        conditions.append(col.ilike(f"%{value}%"))
                    else:
                        conditions.append(col == value)

            if conditions:
                query = query.where(and_(*conditions))

        result = await self.db.execute(query)
        return result.scalar_one()

    async def exists(
        self, id: int, otherFieldQueries: Optional[Dict[str, Any]] = None
    ) -> bool:
        query = select(func.count()).select_from(self.model).filter(self.model.id == id)

        if otherFieldQueries:
            for field, value in otherFieldQueries.items():
                query = query.filter(getattr(self.model, field) == value)

        result = await self.db.execute(query)
        return result.scalar_one() > 0
