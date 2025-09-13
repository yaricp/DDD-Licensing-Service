from uuid import UUID
from typing import List

# --- Application Imports ---
from ....app.queries.license_queries import LicenseQuery

# --- API Imports ---
from ..schemas.license import License
from ..services.utils import BaseMapper


"""
Can not use Bootstrap object in dependencies,
so its defined in each dependency body.
"""

# -----Views-----


async def get_all_licenses() -> List[License]:
    query: LicenseQuery = LicenseQuery()
    query_results = await query.get_all_licenses()
    return BaseMapper.list_to_schema(License, query_results)


async def get_license(id: UUID) -> License:
    query: LicenseQuery = LicenseQuery()
    query_result = await query.get_license(id=id)
    return BaseMapper.to_schema(License, query_result)
