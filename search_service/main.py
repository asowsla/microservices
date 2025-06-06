from fastapi import FastAPI
from contextlib import asynccontextmanager
from typing import AsyncIterator
from API.search import router as search_router
from services.index_init import ensure_index_exists
from configs.db_config import es, INDEX


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    await ensure_index_exists(es=es, index=INDEX)
    yield


app = FastAPI(
    title="search_service API",
    lifespan=lifespan
)


app.include_router(
    search_router, 
    tags=["Search"]
)


@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok", "service": "search-service"}