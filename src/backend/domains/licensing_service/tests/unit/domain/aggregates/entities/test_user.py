# tests/test_user.py

from uuid import uuid4

from backend.domains.licensing_service.domain.aggregates.entities.user import User


def test_make_creates_user_with_id():
    user_id = uuid4()
    user = User.make(user_id=user_id)

    assert user.user_id == user_id
    assert user.email is None
    assert user.tg_id is None
    assert user.superadmin is False
    assert user.tenant_id is None
    assert user.subdivision_id is None


def test_make_super_admin_sets_flag():
    user = User.make(user_id=uuid4())
    assert user.superadmin is False

    user.make_super_admin()
    assert user.superadmin is True


def test_demote_from_super_admin_resets_flag():
    user = User.make(user_id=uuid4())
    user.make_super_admin()
    assert user.superadmin is True

    user.demote_from_super_admin()
    assert user.superadmin is False
