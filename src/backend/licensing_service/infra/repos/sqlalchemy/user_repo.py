from uuid import UUID
from typing import List, Optional, Sequence, Any
from sqlalchemy import insert, select, delete, update, Result, RowMapping, Row

from backend.core.domain.entity import AbstractEntity
from backend.core.infra.database.repositories import (
    SQLAlchemyAbstractRepository
)

from ....domain.aggregates.entities.user import User


from ....domain.services.repos.user_repo import UserRepository


class SQLAlchemyUserRepository(
    SQLAlchemyAbstractRepository, UserRepository
):

    async def get(self, id: UUID) -> Optional[User]:
        result: Result = await self._session.execute(
            select(User).filter_by(user_id=id)
        )
        return result.scalar_one_or_none()

    async def add(self, model: AbstractEntity) -> User:
        result: Result = await self._session.execute(
            insert(User).values(
                **await model.to_dict(exclude={'id'})
            ).returning(User)
        )

        return result.scalar_one()

    async def update(self, id: UUID, model: AbstractEntity) -> User:
        result: Result = await self._session.execute(
            update(User).filter_by(user_id=id).values(
                **await model.to_dict(exclude={'id'})
            ).returning(User)
        )

        return result.scalar_one()

    async def delete(self, id: UUID) -> None:
        await self._session.execute(delete(User).filter_by(user_id=id))

    async def list(self) -> List[User]:
        """
        Returning result object instead of converting to new objects by
        [UserModel(**await r.to_dict()) for r in result.scalars().all()]
        to avoid sqlalchemy.orm.exc.UnmappedInstanceError lately.

        Checking by asserts, that expected return type is equal 
        to fact return type.
        """

        result: Result = await self._session.execute(select(User))
        users: Sequence[Row | RowMapping | Any] = result.scalars().all()

        assert isinstance(users, List)
        for user in users:
            assert isinstance(user, User)

        return users

    async def get_list_for_tenant(self, tenant_id: UUID) -> List[User]:
        """
        Gets list users for tenant by tenant_id
        """
        result: Result = await self._session.execute(
            select(User).filter_by(tenant_id=tenant_id)
        )
        users: Sequence[Row | RowMapping | Any] = result.scalars().all()

        assert isinstance(users, List)
        for user in users:
            assert isinstance(user, User)

        return users

    # async def get_by_email(self, email: str) -> Optional[User]:
    #     result: Result = await self._session.execute(
    #         select(User).filter_by(email=email)
    #     )
    #     return result.scalar_one_or_none()

    # async def get_by_username(self, username: str) -> Optional[User]:
    #     result: Result = await self._session.execute(
    #         select(User).filter_by(username=username)
    #     )
    #     return result.scalar_one_or_none()
