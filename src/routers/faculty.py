from fastapi import APIRouter, Depends

from src.core.dependencies import get_admin_user
from src.crud import FacultyDAO
from src.models import User
from src.schemas import CreateFacultyResponse

router = APIRouter()


@router.post("", summary="Создает факультет")
async def create_faculty(
    name: str,
    db_faculty: FacultyDAO = Depends(FacultyDAO),
    user: User = Depends(get_admin_user),
) -> CreateFacultyResponse:
    faculty = await db_faculty.add({"name": name})

    return CreateFacultyResponse(id=faculty.id, name=faculty.name)


@router.delete("/{faculty_id}", summary="Удаляет факультет")
async def delete_faculty(
    faculty_id: int,
    db_faculty: FacultyDAO = Depends(FacultyDAO),
    user: User = Depends(get_admin_user),
):
    faculty = await db_faculty.delete(model_id=faculty_id)
    return faculty
