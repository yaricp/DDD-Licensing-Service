import pytest_asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    create_async_engine, AsyncSession, async_sessionmaker
)
from sqlalchemy.orm import clear_mappers
from sqlalchemy.pool import NullPool

from backend.core.infra.database.config import database_config
from backend.core.infra.database.metadata import mapper_registry
from backend.domains.licensing_service.infra.adapters.orm import start_mappers


TEST_DB = "test_db"


@pytest_asyncio.fixture(scope="session")
async def engine():
    """
    Fixture creates a test database and tables once per session.
    """
    admin_url = '{}+{}://{}:{}@{}:{}/{}'.format(
        database_config.DATABASE_DIALECT,
        database_config.DATABASE_DRIVER,
        database_config.DATABASE_USER,
        database_config.DATABASE_PASSWORD,
        database_config.DATABASE_HOST,
        database_config.DATABASE_PORT,
        "postgres"
    )
    admin_engine = create_async_engine(admin_url, isolation_level="AUTOCOMMIT")

    async with admin_engine.connect() as conn:
        result = await conn.execute(
            text(f"SELECT 1 FROM pg_database WHERE datname='{TEST_DB}'")
        )
        exists = result.scalar()
        if not exists:
            await conn.execute(text(f'CREATE DATABASE "{TEST_DB}"'))

    await admin_engine.dispose()

    test_url = '{}+{}://{}:{}@{}:{}/{}'.format(
        database_config.DATABASE_DIALECT,
        database_config.DATABASE_DRIVER,
        database_config.DATABASE_USER,
        database_config.DATABASE_PASSWORD,
        database_config.DATABASE_HOST,
        database_config.DATABASE_PORT,
        TEST_DB
    )
    eng = create_async_engine(test_url, echo=False, poolclass=NullPool)

    async with eng.begin() as conn:
        await conn.run_sync(mapper_registry.metadata.create_all)
    start_mappers()

    yield eng

    async with eng.begin() as conn:
        await conn.run_sync(mapper_registry.metadata.drop_all)
    clear_mappers()
    await eng.dispose()


@pytest_asyncio.fixture(autouse=True)
async def clean_db(engine):
    """Cleans all tables before the test"""
    async_session = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    async with async_session() as session:
        tables = list(mapper_registry.metadata.tables.keys())
        if tables:
            await session.execute(
                text(f'TRUNCATE {", ".join(tables)} RESTART IDENTITY CASCADE')
            )
            await session.commit()


@pytest_asyncio.fixture
async def db_session(engine):
    """Creates session fabric for tests"""
    return async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=True
    )
