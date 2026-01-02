from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.v1.router import api_router
from app.core.logging import setup_logging
from app.db.database import init_db_pool, close_db_pool, init_schema

setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize database pool and schema
    await init_db_pool()
    await init_schema()
    yield
    # Shutdown: Close database pool
    await close_db_pool()


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_PREFIX}/openapi.json",
    docs_url=f"{settings.API_PREFIX}/docs",
    redoc_url=None,
    lifespan=lifespan,
)

# CORS: Vite dev server + 배포 도메인들
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_PREFIX)
