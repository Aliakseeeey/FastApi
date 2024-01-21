from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from api.actions.auth import get_current_user_from_token
from api.actions.user import _update_user, _get_user_by_id, _delete_user, _create_new_user
from api.models import UserCreate, ShowUser, DeleteUserResponse, UpdatedUserResponse, UpdatedUserRequest
from db.session import get_db

from uuid import UUID

from logging import getLogger
from db.models import User

logger = getLogger(__name__)

user_router = APIRouter()


@user_router.post("/", response_model=ShowUser)
async def create_user(body: UserCreate, db: AsyncSession = Depends(get_db)) -> ShowUser:
    try:
        return await _create_new_user(body, db)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")


@user_router.delete("/", response_model=DeleteUserResponse)
async def delete_user(
        user_id: UUID,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token),
) -> DeleteUserResponse:
    delete_user_id = await _delete_user(user_id, db)
    if delete_user_id is None:
        raise HTTPException(status_code=404, defaul=f'User with id {user_id} not found.')
    return DeleteUserResponse(delete_user_id=delete_user_id)


@user_router.get("/", response_model=ShowUser)
async def get_user_by_id(
        user_id: UUID,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token),
) -> ShowUser:
    user = await _get_user_by_id(user_id, db)
    if user is None:
        raise HTTPException(status_code=404, defaul=f'User with id {user_id} not found.')
    return user


@user_router.patch("/", response_model=UpdatedUserResponse)
async def update_user_by_id(
        user_id: UUID,
        body: UpdatedUserRequest,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token),
) -> UpdatedUserResponse:
    update_user_param = body.dict(exclude_none=True)
    if update_user_param == {}:
        raise HTTPException(status_code=422, detail="At least one parameter for user update info should be provided")
    user = await _get_user_by_id(user_id, db)
    if user is None:
        raise HTTPException(status_code=422, detail=f"User with {user_id} not found.")
    try:
        updated_user_id = await _update_user(update_user_param=update_user_param, db=db, user_id=user_id)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")
    return UpdatedUserResponse(updated_user_id=updated_user_id)
