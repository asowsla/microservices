from application.core.config import SETTINGS
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker
)


# create database connection URL from settings
POSTGRES_URL = (
    f"postgresql+asyncpg://"
    f"{SETTINGS.POSTGRES_USER}:{SETTINGS.POSTGRES_PASSWORD}@"
    f"{SETTINGS.POSTGRES_HOST}:{SETTINGS.POSTGRES_PORT}/"
    f"{SETTINGS.POSTGRES_DB}"
)


# Create async database engine
engine = create_async_engine(POSTGRES_URL, echo=True)


# configure session factory
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,  # prevents attribute refresh after commit
    autocommit=False,
    autoflush=False
)


# dependency that provides database session
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()