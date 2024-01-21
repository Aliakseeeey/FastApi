from typing import Union
from uuid import UUID

from api.models import ShowUser, UserCreate
from db.dals import UserDAL
from hashing import Hasher


async def _create_new_user(body: UserCreate, session) -> ShowUser:
    async with session.begin():
        user_dal = UserDAL(session)
        user = await user_dal.create_user(
            name=body.name,
            surname=body.surname,
            email=body.email,
            hashed_password=Hasher.get_password_hash(body.password)
        )
        return ShowUser(
            user_id=user.user_id,
            name=user.name,
            surname=user.surname,
            email=user.email,
            is_activ=user.is_activ
        )


async def _delete_user(user_id, session) -> Union[UUID, None]:
    async with session.begin():
        user_dal = UserDAL(session)
        delete_user_id = await user_dal.delete_user(
            user_id=user_id,
        )
        return delete_user_id


async def _update_user(update_user_param: dict, user_id: UUID, session) -> Union[UUID, None]:
    async with session.begin():
        user_dal = UserDAL(session)
        updated_user_id = await user_dal.update_user(
            user_id=user_id,
            **update_user_param
        )
        return updated_user_id


async def _get_user_by_id(user_id, session) -> Union[ShowUser, None]:
    async with session.begin():
        user_dal = UserDAL(session)
        user = await user_dal.get_user_by_id(
            user_id=user_id,
        )
        if user is not None:
            return ShowUser(
                user_id=user.user_id,
                name=user.name,
                surname=user.surname,
                email=user.email,
                is_activ=user.is_activ,
            )
