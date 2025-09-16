from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class UserBase(BaseModel):
    user_id: Optional[UUID] = None
    email: Optional[str] = None
    tg_id: Optional[str] = None
    superadmin: Optional[bool] = False
    tenant_id: Optional[UUID] = None
    subdivision_id: Optional[UUID] = None


class UserCreate(BaseModel):
    user_id: UUID


class User(UserBase):
    pass
