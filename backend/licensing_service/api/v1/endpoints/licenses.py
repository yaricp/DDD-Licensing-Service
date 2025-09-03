from uuid import UUID
from typing import List, MutableSequence
from fastapi import APIRouter, Depends

# --- API Imports ---
from ..schemas.license import License
from ..services.license import (
    get_license, get_all_licenses
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
