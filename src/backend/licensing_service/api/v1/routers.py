from fastapi import APIRouter

from ..config import rest_api_config

from .endpoints import (
    tenants, users, licenses, subdivisions
)

prefix = f"/{rest_api_config.API_PREFIX}/api/v1"

api_router = APIRouter()
api_router.include_router(
    subdivisions.router,
    prefix=f"{prefix}/subdivisions",
    tags=["Subdivisions"]
)
api_router.include_router(
    users.router,
    prefix=f"{prefix}/users",
    tags=["Users"]
)
api_router.include_router(
    tenants.router,
    prefix=f"{prefix}/tenants",
    tags=["Tenants"]
)
api_router.include_router(
    licenses.router,
    prefix=f"{prefix}/licenses",
    tags=["Licenses"]
)
