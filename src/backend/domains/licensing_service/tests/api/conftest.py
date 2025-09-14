from sqlalchemy import text
import pytest_asyncio
import asyncio
import pytest
from httpx import AsyncClient, ASGITransport
from asgi_lifespan import LifespanManager
from infrastructure.rest_api.main import app
from core.infra.database.connection import engine as async_engine
from licensing_service.api.v1.routers import prefix


@pytest.fixture(scope="function")
def async_client():
    """Синхронная фикстура, которая создает async client"""
    async def _create_client():
        transport = ASGITransport(app=app)
        return AsyncClient(transport=transport, base_url=f"http://test{prefix}")
    client = asyncio.run(_create_client())
    yield client
    asyncio.run(client.aclose())


@pytest.fixture(autouse=True)
def clean_db():
    """Простая синхронная очистка"""
    async def _clean():
        async with async_engine.begin() as conn:
            await conn.execute(text("TRUNCATE TABLE tenants CASCADE;"))
    asyncio.run(_clean())
    yield



# @pytest_asyncio.fixture(scope="session")
# async def async_client():
#     async with LifespanManager(app):  # запускаем startup/shutdown
#         transport = ASGITransport(app=app)  # правильный способ передать ASGI-приложение
#         async with AsyncClient(
#             transport=transport, base_url=f"http://test{prefix}"
#         ) as ac:
#             yield ac


# @pytest_asyncio.fixture()
# async def clean_db():
#     """
#     Очищаем таблицы после каждого теста.
#     """
#     async with async_engine.begin() as conn:
#         await conn.execute(
#             text("TRUNCATE TABLE tenants CASCADE;")
#         )
#         await conn.commit()
    #     # Можно добавить другие таблицы
    # yield
    # async with async_engine.begin() as conn:
    #     await conn.execute(
    #         text("TRUNCATE TABLE tenants CASCADE;")
    #     )
    #     await conn.commit()
