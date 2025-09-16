from typing import List, MutableSequence
from uuid import UUID

from fastapi import APIRouter, Depends

# --- API Imports ---
from ...deps import get_messagebus_handler
from ..schemas.user import User
from ..services.user import get_all_users, get_or_create_user

router = APIRouter()


@router.get("/", response_model=List[User])
async def read_users_route():
    """
    Retrieve users.
    """
    users: MutableSequence[User] = await get_all_users()
    return users


@router.get("/get_or_create/{id}", response_model=User)
async def get_or_create_user_route(
    id: UUID, messagebus_handler=Depends(get_messagebus_handler)
):
    user: User = await get_or_create_user(
        user_id=id, messagebus_handler=messagebus_handler
    )
    return user
