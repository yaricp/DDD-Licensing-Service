from uuid import UUID
from typing import List, MutableSequence
from fastapi import APIRouter, Depends

# --- API Imports ---
from ...deps import get_messagebus_handler
from ..schemas.subdivision import (
    Subdivision, SubdivisionCreate, SubdivisionUpdate
)
from ..schemas.license import LicenseCreate, LicenseUpdate
from ..services.subdivision import (
    get_subdivision, active_subdivision_license,
    subdivision_add_statistic_row,
    create_subdivision, get_all_subdivisions,
    update_subdivision, delete_subdivision,
    deactive_subdivision_license,
    subdivision_create_license, subdivision_update_license,
    subdivision_delete_license
)


router = APIRouter()


@router.post(
    "/", name="Create a new Subdivision",
    response_model=Subdivision
)
async def create_subdivision_route(
    *, item_in: SubdivisionCreate,
    messagebus_handler=Depends(get_messagebus_handler)
) -> str:
    """
    Create new subdivision.
    """
    subdivision = await create_subdivision(
        subdivision_data=item_in,
        messagebus_handler=messagebus_handler
    )
    return subdivision


@router.get(
    "/", name="Get All Subdivisions",
    response_model=List[Subdivision]
)
async def get_all_subdivisions_route():
    subdivisions: MutableSequence[
        Subdivision
    ] = await get_all_subdivisions()
    return subdivisions


@router.get(
    "/{id}", name="Get Subdivision",
    response_model=Subdivision
)
async def get_subdivision_route(id: UUID):
    subdivision: Subdivision = await get_subdivision(id=id)
    return subdivision


@router.put(
    "/{id}", name="Update Subdivision",
    response_model=Subdivision
)
async def put_subdivision_route(
    id: UUID, item_in: SubdivisionUpdate,
    messagebus_handler=Depends(get_messagebus_handler)
):
    item_in.id = id
    subdivision: Subdivision = await update_subdivision(
        subdivision_data=item_in,
        messagebus_handler=messagebus_handler
    )
    return subdivision


@router.delete(
    "/{id}", name="Delete Subdivision",
    response_model=Subdivision
)
async def delete_subdivision_route(
    id: UUID,
    messagebus_handler=Depends(get_messagebus_handler)
):
    result: Subdivision = await delete_subdivision(
        id=id, messagebus_handler=messagebus_handler
    )
    return result


@router.put(
    path="/{id}/active_license/{license_id}",
    name="Activate License",
    response_model=Subdivision
)
async def activate_license_route(
    id: UUID, license_id: UUID,
    messagebus_handler=Depends(get_messagebus_handler)
) -> Subdivision:
    subdivision = await active_subdivision_license(
        license_id=license_id, subdivision_id=id,
        messagebus_handler=messagebus_handler
    )
    return subdivision


@router.put(
    path="/{id}/deactive_license/{license_id}",
    name="Deactivate License",
    response_model=Subdivision
)
async def deactivate_license_route(
    id: UUID, license_id: UUID,
    messagebus_handler=Depends(get_messagebus_handler)
) -> Subdivision:
    subdivision = await deactive_subdivision_license(
        license_id=license_id, subdivision_id=id,
        messagebus_handler=messagebus_handler
    )
    return subdivision


@router.post(
    path="/{id}/statistic_row_add",
    name="Add Statistic Row",
    response_model=Subdivision
)
async def statictic_row_add_route(
    id: UUID, count_requests: int,
    messagebus_handler=Depends(get_messagebus_handler)
) -> Subdivision:
    subdivision = await subdivision_add_statistic_row(
        subdivision_id=id, count_requests=count_requests,
        messagebus_handler=messagebus_handler
    )
    return subdivision


@router.post(
    path="/{id}/create_license",
    name="Create a new License",
    response_model=Subdivision
)
async def create_license_route(
    id: UUID, item_in: LicenseCreate,
    messagebus_handler=Depends(get_messagebus_handler)
) -> Subdivision:
    subdivision = await subdivision_create_license(
        license_data=item_in,
        messagebus_handler=messagebus_handler
    )
    return subdivision


@router.put(
    path="/{id}/update_license/{license_id}",
    name="Update License",
    response_model=Subdivision
)
async def update_license_route(
    id: UUID, item_in: LicenseUpdate,
    messagebus_handler=Depends(get_messagebus_handler)
) -> Subdivision:
    subdivision = await subdivision_update_license(
        license_data=item_in,
        messagebus_handler=messagebus_handler
    )
    return subdivision


@router.delete(
    path="/{id}/update_license/{license_id}",
    name="Delete License",
    response_model=Subdivision
)
async def delete_license_route(
    id: UUID, license_id: UUID,
    messagebus_handler=Depends(get_messagebus_handler)
) -> Subdivision:
    subdivision = await subdivision_delete_license(
        subdivision_id=id,
        license_id=license_id,
        messagebus_handler=messagebus_handler
    )
    return subdivision
