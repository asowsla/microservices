from sqlalchemy.ext.asyncio import (AsyncSession,
                                    async_sessionmaker,
                                    create_async_engine
                                )
from elasticsearch import AsyncElasticsearch
from configs.config import get_settings


settings = get_settings()


INDEX = settings.ELASTICSEARCH_INDEX_NAME
SIZE = settings.ELASTICSEARCH_SEARCH_SIZE
INTERVAL = settings.SCHEDULE_INTERVAL_SECONDS
SEARCH_SERVICE_URL = settings.search_service_url
ELASTICSEARCH_URL = settings.elastic_search_url
POSTGRES_URL = settings.postgres_url


engine = create_async_engine(
    POSTGRES_URL,
    echo=True
)


es = AsyncElasticsearch(hosts=[ELASTICSEARCH_URL])


AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)


async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session


async def get_db_session_instance() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        return session