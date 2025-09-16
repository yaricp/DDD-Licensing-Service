from typing import List, Optional
from uuid import UUID

from ...domain.aggregates.tenant import Tenant
from ...domain.exceptions.tenant import TenantNotFoundError

# ---Domain imports---
from ...domain.services.uow.tenant_uow import TenantUnitOfWork

# ---Infrastructure imports---
from ...infra.uow.sqlalchemy.tenant_uow import SQLAlchemyTenantUnitOfWork as UOW

# ---Application imports---
from ..services.tenant_services import TenantService


class TenantQuery:
    """
    Query class use for read info about Subdivision aggregate.
    It's in CQRS paradigme
    """

    def __init__(self) -> None:
        self._uow: TenantUnitOfWork = UOW()

    async def get_tenant_by_id(self, id: UUID) -> Tenant:
        async with self._uow as uow:
            tenant: Optional[Tenant] = await uow.tenants.get(id=id)
            if not tenant:
                raise TenantNotFoundError
            users = await uow.users.get_list_for_tenant(tenant_id=tenant.id)
            tenant = Tenant(tenant=tenant, users=users)
            return tenant

    async def get_tenant(self, tenant_id: UUID) -> Tenant:
        tenants_service: TenantService = TenantService()
        tenant: Tenant = await tenants_service.get_tenant_by_id(id=tenant_id)
        return tenant

    async def get_all_tenants(self) -> List[Tenant]:
        tenants_service: TenantService = TenantService()
        tenants: List[Tenant] = await tenants_service.get_all_tenants()
        return tenants
