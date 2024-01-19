from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.models import UserCreate, ShowUser, DeleteUserResponse, UpdatedUserResponse
from db.dals import UserDAL
from db.session import get_db

from typing import Union
from uuid import UUID

user_router = APIRouter()


async def _create_new_user(body: UserCreate, db) -> ShowUser:
    async with db as session:
        async with session.begin():
            user_dal = UserDAL(session)
            user = await user_dal.create_user(
                name=body.name,
                surname=body.surname,
                email=body.email
            )
            return ShowUser(
                user_id=user.user_id,
                name=user.name,
                surname=user.surname,
                email=user.email,
                is_activ=user.is_activ
            )


async def _delete_user(user_id, db) -> Union[UUID, None]:
    async with db as session:
        async with session.begin():
            user_dal = UserDAL(session)
            delete_user_id = await user_dal.delete_user(
                user_id=user_id,
            )
            return delete_user_id


async def _update_user(body, db) -> Union[UUID, None]:
    async with db as session:
        async with session.begin():
            user_dal = UserDAL(session)
            updated_user_id = await user_dal.update_user(
                **body.dict()
            )
            return updated_user_id


async def _get_user_by_id(user_id, db) -> Union[ShowUser, None]:
    async with db as session:
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
                    is_active=user.is_activ,
                )


@user_router.post("/", response_model=ShowUser)
async def create_user(body: UserCreate, db: AsyncSession = Depends(get_db)) -> ShowUser:
    return await _create_new_user(body, db)


@user_router.delete("/", response_model=DeleteUserResponse)
async def delete_user(user_id: UUID, db: AsyncSession = Depends(get_db)) -> DeleteUserResponse:
    delete_user_id = await _delete_user(user_id, db)
    if delete_user_id is None:
        raise HTTPException(status_code=404, defaul=f'User with id {user_id} not found.')
    return DeleteUserResponse(delete_user_id=delete_user_id)


@user_router.get("/", response_model=ShowUser)
async def get_user_by_id(user_id: UUID, db: AsyncSession = Depends(get_db)) -> ShowUser:
    user = await _get_user_by_id(user_id, db)
    if user is None:
        raise HTTPException(status_code=404, defaul=f'User with id {user_id} not found.')
    return user


@user_router.patch("/", response_model=UpdatedUserResponse)
async def update_user_by_id(
        user_id: UUID, body: UpdatedUserRequest, db: AsyncSession = Depends(get_db)) -> UpdatedUserResponse:
    if body.dict(exclude_none=True) == {}:
        raise HTTPException(status_code=422, detail="At least one parameter for user update info should be provided")
    user = await _get_user_by_id(user_id, db)
    if user is None:
        raise HTTPException(status_code=422, detail=f"User with {user_id} not found.")
    updated_user_id = await _update_user(body=body, db=db)
    return UpdatedUserResponse(updated_user_id=updated_user_id)
