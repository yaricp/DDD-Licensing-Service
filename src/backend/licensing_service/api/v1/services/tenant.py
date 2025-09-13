from uuid import UUID
from typing import List

# --- Core Imports ---
from backend.core.messagebus_handler import GlobalMessageBusHandler

# --- Application Imports ---
# from ....app import Tenant
from ....app.queries.tenant_queries import TenantQuery
from ....app.commands.tenant_commands import TenantCommandUseCase

# --- API Imports ---
from ..schemas.tenant import (
    Tenant, TenantCreate, TenantUpdate
)
from ..schemas.subdivision import Subdivision
from ..services.utils import BaseMapper


"""
Can not use Bootstrap object in dependencies,
so its defined in each dependency body.
"""

# ----Views----


async def get_tenant(id: UUID) -> Tenant:
    tenants_views: TenantQuery = TenantQuery()
    query_result = await tenants_views.get_tenant(tenant_id=id)
    return BaseMapper.to_schema(Tenant, query_result)


async def get_all_tenants() -> List[Tenant]:
    tenants_views: TenantQuery = TenantQuery()
    query_results = await tenants_views.get_all_tenants()
    return BaseMapper.list_to_schema(Tenant, query_results)


# ----Actions(Commands)


async def create_tenant(
    tenant_data: TenantCreate,
    messagebus_handler: GlobalMessageBusHandler
) -> Tenant:
    tenant_command = TenantCommandUseCase(
        messagebus_handler=messagebus_handler
    )
    command_result = await tenant_command.create_tenant(
        **tenant_data.model_dump()
    )
    return BaseMapper.to_schema(Tenant, command_result)


async def update_tenant(
    tenant_data: TenantUpdate,
    messagebus_handler: GlobalMessageBusHandler
) -> Tenant:
    tenant_command = TenantCommandUseCase(
        messagebus_handler=messagebus_handler
    )
    command_result = await tenant_command.update_tenant(
        **tenant_data.model_dump()
    )
    return BaseMapper.to_schema(Tenant, command_result)


async def delete_tenant(
    id: UUID,
    messagebus_handler: GlobalMessageBusHandler
) -> Tenant:
    tenant_command = TenantCommandUseCase(
        messagebus_handler=messagebus_handler
    )
    command_result = await tenant_command.delete_tenant(id=id)
    return BaseMapper.to_schema(Tenant, command_result)
