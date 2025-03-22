from fastapi import APIRouter, Depends

from src.core.dependencies import get_admin_user
from src.crud import GroupDAO
from src.models import User
from src.schemas import CreateGroupResponse

router = APIRouter()


@router.post("", summary="Создает группу")
async def create_group(
    name: str,
    db_group: GroupDAO = Depends(GroupDAO),
    user: User = Depends(get_admin_user),
) -> CreateGroupResponse:
    group = await db_group.add({"name": name})

    return CreateGroupResponse(id=group.id, name=group.name)


@router.delete("/{group_id}", summary="Удаляет группу")
async def delete_group(
    group_id: int,
    db_group: GroupDAO = Depends(GroupDAO),
    user: User = Depends(get_admin_user),
):
    group = await db_group.delete(model_id=group_id)
    return group
