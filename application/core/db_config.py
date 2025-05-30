from redis.asyncio import Redis
from application.core.config import SETTINGS
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


POSTGRES_URL = (
    f"postgresql+asyncpg://"
    f"{SETTINGS.POSTGRES_USER}:{SETTINGS.POSTGRES_PASSWORD}@"
    f"{SETTINGS.POSTGRES_HOST}:{SETTINGS.POSTGRES_PORT}/"
    f"{SETTINGS.POSTGRES_DB}"
)


# Redis connection
REDIS_URL = (
    f"redis://{SETTINGS.REDIS_HOST}:"
    f"{SETTINGS.REDIS_PORT}/0"
)


async_engine = create_async_engine(POSTGRES_URL, echo=True)


AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


# provides database session
async def get_db_session():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


# Redis client setup
redis_client = Redis.from_url(
    REDIS_URL,
    encoding="utf-8",
    decode_responses=True
)


def get_redis() -> Redis:
    return redis_client