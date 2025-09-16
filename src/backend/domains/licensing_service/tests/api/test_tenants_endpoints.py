import asyncio
from uuid import UUID

import pytest


@pytest.mark.asyncio
async def test_create_tenant(async_client, clean_db):
    response = await async_client.get(
        "/users/get_or_create/3fa85f64-5717-4562-b3fc-2c963f66afa6"
    )
    print(f"response: {response}")
    print(f"response.status_code: {response.status_code}")
    assert response.status_code == 200
    response = await async_client.post(
        "/tenants/",
        json={
            "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "name": "TestTenant",
            "address": "Address123123",
            "email": "email1@co.com",
            "phone": "123123123",
        },
    )
    print(f"response: {response}")
    print(f"response.status_code: {response.status_code}")
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["name"] == "TestTenant"
    return data["id"]


@pytest.mark.asyncio
async def test_get_all_tenants(async_client):
    response = await async_client.get("/tenants/")
    assert response.status_code == 200
    tenants = response.json()
    assert isinstance(tenants, list)


@pytest.mark.asyncio
async def test_get_tenant(async_client, clean_db):
    response = await async_client.get(
        "/users/get_or_create/3fa85f64-5717-4562-b3fc-2c963f66afa6"
    )
    print(f"response: {response}")
    print(f"response.status_code: {response.status_code}")
    assert response.status_code == 200
    create_resp = await async_client.post(
        "/tenants/",
        json={
            "name": "AnotherTenant4234234",
            "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "address": "Address12334234",
            "email": "email2@co.com",
            "phone": "34534534535",
        },
    )
    tenant_id = create_resp.json()["id"]

    # потом получаем
    response = await async_client.get(f"/tenants/{tenant_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == tenant_id


@pytest.mark.asyncio
async def test_update_tenant(async_client, clean_db):
    # создаём
    response = await async_client.get(
        "/users/get_or_create/3fa85f64-5717-4562-b3fc-2c963f66afa7"
    )
    print(f"response: {response}")
    print(f"response.status_code: {response.status_code}")
    assert response.status_code == 200
    create_resp = await async_client.post(
        "/tenants/",
        json={
            "name": "Anothe5345345",
            "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "address": "Addreadsffds4",
            "email": "email3@co.com",
            "phone": "345asdasdasdasd35",
        },
    )
    tenant_id = create_resp.json()["id"]

    # апдейтим
    response = await async_client.put(
        f"/tenants/{tenant_id}",
        json={
            "name": "TenantUpdated",
            "address": "AddreadsUpdate",
            "email": "email4@co.com",
            "phone": "345asUpdate",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "TenantUpdated"
    assert data["address"] == "AddreadsUpdate"
    assert data["email"] == "email4@co.com"
    assert data["phone"] == "345asUpdate"


@pytest.mark.asyncio
async def test_delete_tenant(async_client, clean_db):
    # создаём
    response = await async_client.get(
        "/users/get_or_create/3fa85f64-5717-4562-b3fc-2c963f66afa6"
    )
    print(f"response: {response}")
    print(f"response.status_code: {response.status_code}")
    assert response.status_code == 200
    create_resp = await async_client.post(
        "/tenants/", json={"name": "TenantToDelete", "address": "Tmp"}
    )
    tenant_id = create_resp.json()["id"]

    # удаляем
    response = await async_client.delete(f"/tenants/{tenant_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == tenant_id

    # проверяем, что больше не доступен
    response = await async_client.get(f"/tenants/{tenant_id}")
    assert response.status_code in (404, 400)  # зависит от реализации
