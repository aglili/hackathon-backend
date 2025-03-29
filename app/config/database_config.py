import os
import signal
import asyncio

import structlog
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncEngine
from sqlalchemy.ext.declarative import declarative_base

from app.config.settings import settings

LOG = structlog.get_logger()


engine: AsyncEngine = create_async_engine(
    settings.DB_URI.replace('postgresql://', 'postgresql+asyncpg://'),
    connect_args={
        "statement_cache_size": 0,
        "prepared_statement_cache_size": 0
    }
)

# Create async session factory
async_sessionLocal = async_sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

Base = declarative_base()

async def ping_database():
    """Async database ping method."""
    try:
        async with engine.begin() as conn:
            LOG.info("Pinged the database")
    except Exception as e:
        LOG.critical("Failed pinging database", error=str(e))
        os.kill(os.getpid(), signal.SIGTERM)

async def get_db():
    """Async database session generator."""
    async with async_sessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()

async def init_db():
    """Async database initialization."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
