from fastapi import APIRouter, Depends

from src.core.dependencies import get_admin_user
from src.crud import GroupDAO
from src.models import User
from src.schemas import CreateGroupResponse

router = APIRouter()


@router.post("", summary="Create group")
async def create_group(
    name: str,
    db_group: GroupDAO = Depends(GroupDAO),
    user: User = Depends(get_admin_user),
) -> CreateGroupResponse:
    """Creates a new group in the system.

    Args:
        name (str): Group name
        db_group (GroupDAO): DAO for working with groups
        user (User): Authorized administrator

    Returns:
        CreateGroupResponse: Created group

    Raises:
        HTTPException: 403 if user is not an administrator
    """
    group = await db_group.add({"name": name})

    return CreateGroupResponse(id=group.id, name=group.name)


@router.delete("/{group_id}", summary="Delete group")
async def delete_group(
    group_id: int,
    db_group: GroupDAO = Depends(GroupDAO),
    user: User = Depends(get_admin_user),
) -> bool:
    """Deletes a group from the system.

    Args:
        group_id (int): Unique group identifier
        db_group (GroupDAO): DAO for working with groups
        user (User): Authorized administrator

    Returns:
        bool: True if deletion was successful

    Raises:
        HTTPException:
            403 if user is not an administrator
            404 if group is not found
    """
    group = await db_group.delete(model_id=group_id)
    return group
