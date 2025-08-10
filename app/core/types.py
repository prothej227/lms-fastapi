from typing import TypeVar
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
from pydantic import BaseModel


class RecordTypeModel(Base):
    __abstract__ = True
    id: Mapped[int] = mapped_column(primary_key=True)


RecordType = TypeVar("RecordType", bound=RecordTypeModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
