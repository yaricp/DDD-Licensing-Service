from uuid import UUID
from typing import List

# --- Core Imports ---
from backend.core.messagebus_handler import GlobalMessageBusHandler

# --- Application Imports ---
# from ....app import License
from ....app.queries.license_queries import LicenseQuery
from ....app.commands.license_commands import LicenseCommandUseCase

# --- API Imports ---
from ..schemas.license import License, LicenseCreate, LicenseUpdate
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


# ------Actons(Commands)-------


async def create_license(
    license_data: LicenseCreate,
    messagebus_handler: GlobalMessageBusHandler
) -> License:
    command = LicenseCommandUseCase(
        messagebus_handler=messagebus_handler
    )
    command_result = await command.create_license(
        **license_data.model_dump()
    )

    return BaseMapper.to_schema(License, command_result)


async def update_license(
    id: UUID, license_data: LicenseUpdate,
    messagebus_handler: GlobalMessageBusHandler
) -> License:

    command = LicenseCommandUseCase(
        messagebus_handler=messagebus_handler
    )
    command_result = await command.update_license(
        **license_data.model_dump()
    )
    return BaseMapper.to_schema(License, command_result)


async def delete_license(
    id: UUID,
    messagebus_handler: GlobalMessageBusHandler
) -> License:
    command = LicenseCommandUseCase(
        messagebus_handler=messagebus_handler
    )
    command_result = await command.delete_license(id=id)
    return BaseMapper.to_schema(License, command_result)
