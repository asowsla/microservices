from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlmodel import SQLModel
from sqlalchemy import text
from application.core.db_config import async_engine, redis_client
from application.routes import auths, users


# management for startup/shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    async with async_engine.connect() as conn:
        await conn.execute(text("SELECT 1"))
    
    await redis_client.ping()
    
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(auths.router)
app.include_router(users.router)

@app.get("/health")
async def health_check():
    return {"status": "ok"}