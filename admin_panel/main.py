from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlmodel import SQLModel
from sqlalchemy import text
from shared.core.db_config import engine
from API import products


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.connect() as conn:
        await conn.execute(text("SELECT 1"))

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    yield


app = FastAPI(
    title="Admin Panel API",
    description="API for administrative product control",
    lifespan=lifespan
)


# connecting routers
app.include_router(products.router)


@app.get("/health", tags=["Health"])
async def health_check() -> dict[str, str]:
    return {"status": "ok", "service": "admin_panel"}