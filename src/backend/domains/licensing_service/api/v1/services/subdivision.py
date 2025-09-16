from datetime import datetime
from typing import List
from uuid import UUID

# --- Core Imports ---
from backend.core.messagebus_handler import GlobalMessageBusHandler

from ....app.commands.subdivision_commands import SubdivisionCommandUseCase

# --- Application Imports ---
# from ....app import Subdivision
from ....app.queries.subdivision_queries import SubdivisionQuery
from ..schemas.license import LicenseCreate, LicenseUpdate

# --- API Imports ---
from ..schemas.subdivision import Subdivision, SubdivisionCreate, SubdivisionUpdate
from ..services.utils import BaseMapper

# ----Views----


async def get_subdivision(id: UUID) -> Subdivision:
    subdivisions_query = SubdivisionQuery()
    query_result = await subdivisions_query.get_subdivision_by_id(id=id)
    return BaseMapper.to_schema(Subdivision, query_result)


async def get_all_subdivisions() -> List[Subdivision]:
    subdivisions_views: SubdivisionQuery = SubdivisionQuery()
    query_results = await subdivisions_views.get_all_subdivisions()
    return BaseMapper.list_to_schema(Subdivision, query_results)


# ----Actions(Commands)


async def active_subdivision_license(
    subdivision_id: UUID, license_id: UUID, messagebus_handler: GlobalMessageBusHandler
) -> Subdivision:
    command = SubdivisionCommandUseCase(messagebus_handler=messagebus_handler)
    command_result = await command.active_subdivision_license(
        subdivision_id=subdivision_id, license_id=license_id
    )
    return BaseMapper.to_schema(Subdivision, command_result)


async def deactive_subdivision_license(
    subdivision_id: UUID, license_id: UUID, messagebus_handler: GlobalMessageBusHandler
) -> Subdivision:
    command = SubdivisionCommandUseCase(messagebus_handler=messagebus_handler)
    command_result = await command.deactive_subdivision_license(
        subdivision_id=subdivision_id, license_id=license_id
    )
    return BaseMapper.to_schema(Subdivision, command_result)


async def subdivision_add_statistic_row(
    subdivision_id: UUID,
    count_requests: int,
    messagebus_handler: GlobalMessageBusHandler,
) -> Subdivision:
    command = SubdivisionCommandUseCase(messagebus_handler=messagebus_handler)
    command_result = await command.subdivision_add_stat_row(
        created=datetime.now(),
        subdivision_id=subdivision_id,
        count_requests=count_requests,
    )
    return BaseMapper.to_schema(Subdivision, command_result)


async def create_subdivision(
    subdivision_data: SubdivisionCreate, messagebus_handler: GlobalMessageBusHandler
) -> Subdivision:
    subdivision_command = SubdivisionCommandUseCase(
        messagebus_handler=messagebus_handler
    )
    command_result = await subdivision_command.create_subdivision(
        **subdivision_data.model_dump()
    )
    return BaseMapper.to_schema(Subdivision, command_result)


async def update_subdivision(
    subdivision_data: SubdivisionUpdate, messagebus_handler: GlobalMessageBusHandler
) -> Subdivision:
    subdivision_command = SubdivisionCommandUseCase(
        messagebus_handler=messagebus_handler
    )
    command_result = await subdivision_command.update_subdivision(
        **subdivision_data.model_dump()
    )
    return BaseMapper.to_schema(Subdivision, command_result)


async def delete_subdivision(
    id: UUID, messagebus_handler: GlobalMessageBusHandler
) -> Subdivision:
    subdivision_command = SubdivisionCommandUseCase(
        messagebus_handler=messagebus_handler
    )
    command_result = await subdivision_command.delete_subdivision(id=id)
    return BaseMapper.to_schema(Subdivision, command_result)


async def subdivision_create_license(
    license_data: LicenseCreate, messagebus_handler: GlobalMessageBusHandler
) -> Subdivision:
    command = SubdivisionCommandUseCase(messagebus_handler=messagebus_handler)
    command_result = await command.subdivision_create_license(
        **license_data.model_dump()
    )
    return BaseMapper.to_schema(Subdivision, command_result)


async def subdivision_update_license(
    license_data: LicenseUpdate, messagebus_handler: GlobalMessageBusHandler
) -> Subdivision:
    command = SubdivisionCommandUseCase(messagebus_handler=messagebus_handler)
    command_result = await command.subdivision_update_license(
        **license_data.model_dump()
    )
    return BaseMapper.to_schema(Subdivision, command_result)


async def subdivision_delete_license(
    subdivision_id: UUID, license_id: UUID, messagebus_handler: GlobalMessageBusHandler
) -> Subdivision:
    command = SubdivisionCommandUseCase(messagebus_handler=messagebus_handler)
    command_result = await command.subdivision_delete_license(
        id=license_id, subdivision_id=subdivision_id
    )
    return BaseMapper.to_schema(Subdivision, command_result)
