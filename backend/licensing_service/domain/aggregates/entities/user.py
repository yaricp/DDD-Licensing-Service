from uuid import UUID
from typing import Optional
from dataclasses import dataclass

from backend.core.domain.entity import AbstractEntity


@dataclass(eq=False, slots=True)
class User(AbstractEntity):

    user_id: UUID
    email: Optional[str] = None
    tg_id: Optional[str] = None
    superadmin: Optional[bool] = False
    tenant_id: Optional[UUID] = None
    subdivision_id: Optional[UUID] = None

    def make_super_admin(self):
        self.superadmin = True

    def demote_from_super_admin(self):
        self.superadmin = False
