from typing import List, MutableSequence
from uuid import UUID

from fastapi import APIRouter, Depends

# --- API Imports ---
from ...deps import get_messagebus_handler
from ..schemas.tenant import Tenant, TenantCreate, TenantUpdate
from ..services.tenant import (
    create_tenant,
    delete_tenant,
    get_all_tenants,
    get_tenant,
    update_tenant,
)

router = APIRouter()


@router.post("/", name="Create a new Tenant", response_model=Tenant)
async def create_tenant_route(
    *, item_in: TenantCreate, messagebus_handler=Depends(get_messagebus_handler)
) -> Tenant:
    """
    Create new tenant.
    """
    tenant = await create_tenant(
        tenant_data=item_in, messagebus_handler=messagebus_handler
    )
    return tenant


@router.get("/", name="Get All Tenants", response_model=List[Tenant])
async def get_all_tenants_route():
    tenants: MutableSequence[Tenant] = await get_all_tenants()
    return tenants


@router.get("/{id}", name="Get Tenant", response_model=Tenant)
async def get_tenant_route(id: UUID):
    tenant: Tenant = await get_tenant(id=id)
    return tenant


@router.put("/{id}", name="Update Tenant", response_model=Tenant)
async def update_tenant_route(
    id: UUID, item_in: TenantUpdate, messagebus_handler=Depends(get_messagebus_handler)
):
    tenant: Tenant = await update_tenant(
        tenant_data=item_in, messagebus_handler=messagebus_handler
    )
    return tenant


@router.delete("/{id}", name="Delete Tenant", response_model=Tenant)
async def delete_tenant_route(
    id: UUID, messagebus_handler=Depends(get_messagebus_handler)
):
    tenant: Tenant = await delete_tenant(id=id, messagebus_handler=messagebus_handler)
    return tenant


# @router.get(
#     path="/{id}/licenses/",
#     name="Get all Tenant Licenses",
#     response_model=Tenant
# )
# async def get_tenant_aggregate_route(id: UUID) -> Tenant:
#     tenant_aggregate: Tenant = await get_tenant_aggregate(
#         id=id
#     )
#     return tenant_aggregate


# @router.post(
#     path="/{id}/licenses/",
#     name="Create a new License",
#     response_model=Tenant
# )
# async def statictic_row_add_route(
#     new_tenant_aggregate: TenantAggregateCreate
# ) -> Tenant:
#     tenant_aggregate = await create_tenant_aggregate(
#         new_tenant_aggregate=new_tenant_aggregate
#     )
#     return tenant_aggregate
