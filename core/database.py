from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from config import settings

engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,
    pool_pre_ping=True,   # test connection before use, discard if dead
    pool_recycle=280,     # recycle before Supabase's ~300s idle timeout
    pool_size=10,
    max_overflow=20,
)

async_session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    pass


@asynccontextmanager
async def get_session():
    """Async context manager for DB sessions with auto-commit/rollback."""
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


async def init_db():
    """Create all tables on startup."""
    from core import models  # noqa: F401 — ensures models are registered
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)