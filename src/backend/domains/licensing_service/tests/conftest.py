import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import (
    create_async_engine, AsyncSession, async_sessionmaker
)
from sqlalchemy.orm import clear_mappers
from backend.core.infra.database.connection import DATABASE_URL
from backend.domains.licensing_service.infra.adapters.orm import start_mappers


@pytest.fixture(scope="session", autouse=True)
def init_mappers():
    clear_mappers()
    start_mappers()


@pytest_asyncio.fixture(scope="session")
async def engine():
    eng = create_async_engine(DATABASE_URL, echo=True)
    yield eng
    await eng.dispose()


@pytest_asyncio.fixture
async def async_session(engine):
    """Создаем новый AsyncSession для каждого теста и очищаем таблицы."""
    async_session_maker = async_sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )
    yield async_session_maker
    async with async_session_maker() as session:
        await session.execute(
            "TRUNCATE tenants, subdivisions, users, lisenses, statistic_rows CASCADE"
        )
        await session.commit()


@pytest.fixture
def uow_factory(engine):
    async_session_maker = async_sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )
    return async_session_maker
