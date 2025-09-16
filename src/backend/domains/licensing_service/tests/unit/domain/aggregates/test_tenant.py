# tests/test_tenant.py

from uuid import uuid4

from backend.domains.licensing_service.domain.aggregates.entities.user import User
from backend.domains.licensing_service.domain.aggregates.tenant import Tenant


def test_make_creates_tenant_with_user():
    user_id = uuid4()
    tenant = Tenant.make(
        user_id=user_id,
        name="Tenant1",
        address="123 Main St",
        email="tenant1@example.com",
        phone="1234567890",
    )

    assert tenant.name == "Tenant1"
    assert tenant.address == "123 Main St"
    assert tenant.email == "tenant1@example.com"
    assert tenant.phone == "1234567890"
    assert len(tenant.users) == 1
    assert isinstance(tenant.users[0], User)
    assert tenant.subdivisions == []


def test_make_from_persistence_restores_aggregate():
    user_id = uuid4()
    user = User.make(user_id)
    subdivisions = []
    tenant = Tenant.make_from_persistence(
        id=uuid4(),
        name="Tenant2",
        address="456 Second St",
        email="tenant2@example.com",
        phone="0987654321",
        users=[user],
        subdivisions=subdivisions,
    )

    assert tenant.name == "Tenant2"
    assert tenant.address == "456 Second St"
    assert tenant.email == "tenant2@example.com"
    assert tenant.phone == "0987654321"
    assert tenant.users == [user]
    assert tenant.subdivisions == subdivisions


def test_update_changes_fields():
    user_id = uuid4()
    tenant = Tenant.make(
        user_id=user_id,
        name="OldTenant",
        address="Old Address",
        email="old@example.com",
        phone="1111111111",
    )

    tenant.update(
        name="NewTenant",
        address="New Address",
        email="new@example.com",
        phone="2222222222",
    )

    assert tenant.name == "NewTenant"
    assert tenant.address == "New Address"
    assert tenant.email == "new@example.com"
    assert tenant.phone == "2222222222"
