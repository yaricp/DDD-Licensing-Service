from uuid import UUID
from typing import List, MutableSequence
from fastapi import APIRouter, Depends

# --- API Imports ---
from ...deps import get_messagebus_handler
from ..schemas.license import (
    License, LicenseUpdate
)
from ..services.license import (
    get_license, get_all_licenses,
    update_license, delete_license
)

router = APIRouter()


@router.get("/", response_model=List[License])
async def get_all_licenses_route():
    licenses: MutableSequence[License] = await get_all_licenses()
    return licenses


@router.get("/{id}", response_model=License)
async def get_license_route(id: UUID):
    license: License = await get_license(id=id)
    return license


@router.put("/{id}", response_model=License)
async def update_license_route(
    id: UUID, item_in: LicenseUpdate,
    messagebus_handler=Depends(get_messagebus_handler)
):
    license: License = await update_license(
        id=id, license_data=item_in, messagebus_handler=messagebus_handler
    )
    return license


@router.delete("/{id}", response_model=License)
async def delete_license_route(
    id: UUID,
    messagebus_handler=Depends(get_messagebus_handler)
):
    license: License = await delete_license(
        id=id, messagebus_handler=messagebus_handler
    )
    return license
