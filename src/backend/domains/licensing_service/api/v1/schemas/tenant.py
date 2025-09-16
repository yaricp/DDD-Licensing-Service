from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel

from .subdivision import Subdivision
from .user import User


class TenantBase(BaseModel):
    id: Optional[UUID] = None
    name: Optional[str] = None
    address: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    users: List[User] = []
    subdivisions: List[Subdivision] = []


class TenantCreate(BaseModel):
    user_id: UUID
    name: str
    address: str
    email: str
    phone: str


class TenantUpdate(TenantBase):
    id: UUID


class TenantStored(TenantBase):
    id: UUID
    name: str
    address: str
    email: str
    phone: str
    users: List[User]
    subdivisions: List[Subdivision]


class Tenant(TenantStored):
    pass
