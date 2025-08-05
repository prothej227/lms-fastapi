from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from typing import AsyncGenerator
from .core.config import get_settings

settings = get_settings()

engine = create_async_engine(
    settings.database_uri,
    connect_args=settings.database_connect_args,
    echo=settings.database_echo,
)
SessionLocal = async_sessionmaker(engine)
Base = declarative_base()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as db:
        try:
            yield db
        except Exception:
            await db.rollback()
            raise
