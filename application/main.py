from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlmodel import SQLModel
from application.core.db_config import engine
from application.api_routes import students, groups


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield


def create_application() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    app.include_router(students.router)
    app.include_router(groups.router)
    return app

app = create_application()

@app.get("/health", tags=["healthcheck"])
async def health_check() -> dict[str, str]:
    return {"status": "ok"}