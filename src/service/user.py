from fastapi import Depends, HTTPException

from src.crud import UserDAO
from src.models import User
from src.models.enum import UserRoleEnum
from src.schemas import GetAllUsersResponse, UserInfo, UpdateUserRequest


class UserService:
    """Service for managing user operations using the DAO layer.

    Provides a complete cycle of working with user data: retrieving information,
    updating profiles, activating and deactivating users.
    """

    def __init__(self, user_dao: UserDAO = Depends()):
        """Initializes DAO for working with users.

        Args:
            user_dao (UserDAO): DAO for working with users
        """
        self._user_dao = user_dao

    async def get_all_users(self, current_user: User) -> GetAllUsersResponse:
        """Returns a list of all active users in the system.

        Args:
            current_user (User): Authorized user

        Returns:
            GetAllUsersResponse: List of active users

        Raises:
            HTTPException: 403 if user is not an administrator
        """
        if current_user.user_role != UserRoleEnum.ADMIN:
            raise HTTPException(status_code=403, detail="Only admin can get all users")

        users = await self._user_dao.find_all(is_active=True)
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

    async def get_user_by_id(self, user_id: int) -> UserInfo:
        """Gets user information by their ID.

        Args:
            user_id (int): Unique user identifier

        Returns:
            UserInfo: User information

        Raises:
            HTTPException: 404 if user is not found
        """
        user = await self._user_dao.find_one(id=user_id)
        return UserInfo(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
            user_role=user.user_role,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )

    async def update_user(
        self, user_id: int, update_data: UpdateUserRequest, current_user: User
    ) -> UserInfo:
        """Updates user information.

        Args:
            user_id (int): Unique user identifier
            update_data (UpdateUserRequest): Data to update
            current_user (User): Authorized user

        Returns:
            UserInfo: Updated user information

        Raises:
            HTTPException:
                403 if user tries to update someone else's profile
                404 if user is not found
        """
        if (current_user.id != user_id) and (
            current_user.user_role != UserRoleEnum.ADMIN
        ):
            raise HTTPException(status_code=403, detail="You can only update yourself.")

        update_data = update_data.dict(exclude_none=True)

        if update_data:
            await self._user_dao.update(model_id=user_id, **update_data)

        user = await self._user_dao.find_one(id=user_id)

        return UserInfo(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
            user_role=user.user_role,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )

    async def deactivate_user(self, user_id: int, current_user: User) -> bool:
        """Deactivates a user in the system.

        Args:
            user_id (int): Unique user identifier
            current_user (User): Authorized user

        Returns:
            bool: True if deactivation was successful

        Raises:
            HTTPException:
                403 if user tries to deactivate someone else's profile
                404 if user is not found
        """
        if (current_user.id != user_id) and (
            current_user.user_role != UserRoleEnum.ADMIN
        ):
            raise HTTPException(status_code=403, detail="You can only delete yourself.")

        await self._user_dao.update(model_id=user_id, is_active=False)
        return True

    async def activate_user(self, user_id: int, current_user: User) -> bool:
        """Activates a user in the system.

        Args:
            user_id (int): Unique user identifier
            current_user (User): Authorized user

        Returns:
            bool: True if activation was successful

        Raises:
            HTTPException:
                403 if user is not an administrator
                404 if user is not found
        """
        if current_user.user_role != UserRoleEnum.ADMIN:
            raise HTTPException(status_code=403, detail="Only ADMIN can activate user")

        await self._user_dao.update(model_id=user_id, is_active=True)
        return True
