from fastapi import APIRouter, Depends

from src.core.dependencies import get_current_user
from src.models import User
from src.schemas import GetAllUsersResponse, UserInfo, UpdateUserRequest
from src.service import UserService

router = APIRouter()


@router.post("", summary="Returns all active users")
async def get_all(
    user_service: UserService = Depends(UserService),
    user: User = Depends(get_current_user),
) -> GetAllUsersResponse:
    """Returns a list of all active users in the system.

    Args:
        user_service (UserService): Service for working with users
        user (User): Authorized user

    Returns:
        GetAllUsersResponse: List of active users

    Raises:
        HTTPException: 403 if user is not an administrator
    """
    return await user_service.get_all_users(current_user=user)


@router.get("/{user_id}", summary="Returns user by id")
async def get_by_id(
    user_id: int, user_service: UserService = Depends(UserService)
) -> UserInfo:
    """Gets user information by their ID.

    Args:
        user_id (int): Unique user identifier
        user_service (UserService): Service for working with users

    Returns:
        UserInfo: User information

    Raises:
        HTTPException: 404 if user is not found
    """
    return await user_service.get_user_by_id(user_id=user_id)


@router.put("/{user_id}", summary="Update user profile")
async def update_user(
    user_id: int,
    updated_user: UpdateUserRequest,
    user_service: UserService = Depends(UserService),
    user: User = Depends(get_current_user),
) -> UserInfo:
    """Updates user information.

    Args:
        user_id (int): Unique user identifier
        updated_user (UpdateUserRequest): Data to update
        user_service (UserService): Service for working with users
        user (User): Authorized user

    Returns:
        UserInfo: Updated user information

    Raises:
        HTTPException:
            403 if user tries to update someone else's profile
            404 if user is not found
    """
    return await user_service.update_user(
        user_id=user_id, update_data=updated_user, current_user=user
    )


@router.delete("/deactivate/{user_id}", summary="Deactivates user by ID")
async def deactivate_by_id(
    user_id: int,
    user_service: UserService = Depends(UserService),
    user: User = Depends(get_current_user),
) -> bool:
    """Deactivates a user in the system.

    Args:
        user_id (int): Unique user identifier
        user_service (UserService): Service for working with users
        user (User): Authorized user

    Returns:
        bool: True if deactivation was successful

    Raises:
        HTTPException:
            403 if user tries to deactivate someone else's profile
            404 if user is not found
    """
    return await user_service.deactivate_user(user_id=user_id, current_user=user)


@router.patch("/activate/{user_id}", summary="Activates user by ID")
async def activate_by_id(
    user_id: int,
    user_service: UserService = Depends(UserService),
    user: User = Depends(get_current_user),
) -> bool:
    """Activates a user in the system.

    Args:
        user_id (int): Unique user identifier
        user_service (UserService): Service for working with users
        user (User): Authorized user

    Returns:
        bool: True if activation was successful

    Raises:
        HTTPException:
            403 if user is not an administrator
            404 if user is not found
    """
    return await user_service.activate_user(user_id=user_id, current_user=user)
