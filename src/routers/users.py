from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Response, Cookie

from src.core.dependencies import get_current_user
from src.crud import UserDAO
from src.models import User
from src.models.enum import UserRoleEnum
from src.schemas import GetAllUsersResponse, UserInfo, UpdateUserRequest

router = APIRouter()


@router.post("", summary="Возвращает всех активных пользователей")
async def get_all(
    db_user: UserDAO = Depends(UserDAO), user: User = Depends(get_current_user)
) -> GetAllUsersResponse:
    if user.username != UserRoleEnum.ADMIN:
        raise HTTPException(status_code=403, detail="Only admin cat get all users")
    users = await db_user.find_all(is_active=True)

    users_response = [
        UserInfo(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
            user_role=user.user_role,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
        for user in users
    ]

    return GetAllUsersResponse(users=users_response)


@router.get("/{user_id}", summary="Возвращает пользователя по id")
async def get_by_id(user_id: int, db_user: UserDAO = Depends(UserDAO)) -> UserInfo:
    user = await db_user.find_one(id=user_id)
    return UserInfo(
        id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username,
        user_role=user.user_role,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )


@router.put("/{user_id}", summary="Обновление профиля пользователя")
async def update_user(
    user_id: int,
    updated_user: UpdateUserRequest,
    db_user: UserDAO = Depends(UserDAO),
    user: User = Depends(get_current_user),
) -> UserInfo:
    if (user.id != user_id) and (user.user_role != UserRoleEnum.ADMIN):
        raise HTTPException(status_code=403, detail="You can only update yourself.")
    update_data = updated_user.dict(exclude_none=True)

    if update_data:
        user_list = await db_user.update(model_id=user_id, **update_data)
        user = user_list[0]
    else:
        user = await db_user.find_one(id=user_id)

    return UserInfo(
        id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username,
        user_role=user.user_role,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )


@router.delete("/deactivate/{user_id}", summary="Деактивирует пользователя по ID")
async def deactivate_by_id(
    user_id: int,
    user: User = Depends(get_current_user),
    db_user: UserDAO = Depends(UserDAO),
) -> bool:
    if (user.id != user_id) and (user.user_role != UserRoleEnum.ADMIN):
        raise HTTPException(status_code=403, detail="You can only delete yourself.")
    await db_user.update(model_id=user_id, is_active=False)
    return True


@router.patch("/activate/{user_id}", summary="Активирует пользователя по ID")
async def activate_by_id(
    user_id: int,
    user: User = Depends(get_current_user),
    db_user: UserDAO = Depends(UserDAO),
) -> bool:
    if user.user_role != UserRoleEnum.ADMIN:
        raise HTTPException(status_code=403, detail="Only ADMIN can activate user")
    await db_user.update(model_id=user_id, is_active=True)
    return True
