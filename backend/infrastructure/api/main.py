from contextlib import asynccontextmanager
from typing import AsyncGenerator
from sqlalchemy.orm import clear_mappers

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from backend.core.infra.database.connection import DATABASE_URL
from backend.core.infra.database.metadata import metadata

from .config import cors_config

from backend.licensing_service.api.v1.routers import (
    api_router as licensing_service_router
)

from backend.licensing_service.infra.adapters.orm import (
    start_mappers as start_tenants_mappers
)
# from backend.licensing_service.infra.adapters.kafka_adapter import (
#     create_topics
# )


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator:
    """
    Runs events before application startup and after application shutdown.
    """

    # Startup events:
    engine: AsyncEngine = create_async_engine(DATABASE_URL)
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)

    start_tenants_mappers()
    # topics=KAFKA_TOPICS, kafka_servers=KAFKA_SERVERS
    # create_topics()

    yield

    # Shutdown events:
    clear_mappers()


app = FastAPI(lifespan=lifespan)

# Middlewares:
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_config.ALLOW_ORIGINS,
    allow_credentials=cors_config.ALLOW_CREDENTIALS,
    allow_methods=cors_config.ALLOW_METHODS,
    allow_headers=cors_config.ALLOW_HEADERS,
)

# Routers:
app.include_router(licensing_service_router)
