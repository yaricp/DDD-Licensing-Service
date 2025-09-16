from typing import List
from uuid import UUID

# --- Core Imports ---
from backend.core.messagebus_handler import GlobalMessageBusHandler

# --- Application Imports ---
# from ....app import User
from ....app.queries.user_queries import UserQuery

# --- API Imports ---
from ..schemas.user import User
from ..services.utils import BaseMapper

"""
Can not use Bootstrap object in dependencies,
so its defined in each dependency body.
"""

# -------Views---------


async def get_all_users() -> List[User]:
    users_views: UserQuery = UserQuery()
    query_results = await users_views.get_all_users()
    return BaseMapper.list_to_schema(User, query_results)


# --------Actions (commands) ---------


async def get_or_create_user(
    user_id: UUID, messagebus_handler: GlobalMessageBusHandler
) -> User:
    user_queries = UserQuery()
    command_result = await user_queries.get_or_create_user(
        user_id=user_id, messagebus_handler=messagebus_handler
    )
    return BaseMapper.to_schema(User, command_result)
