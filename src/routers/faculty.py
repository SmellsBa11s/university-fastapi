from fastapi import APIRouter, Depends

from src.core.dependencies import get_admin_user
from src.crud import FacultyDAO
from src.models import User
from src.schemas import CreateFacultyResponse

router = APIRouter()


@router.post("", summary="Create faculty")
async def create_faculty(
    name: str,
    db_faculty: FacultyDAO = Depends(FacultyDAO),
    user: User = Depends(get_admin_user),
) -> CreateFacultyResponse:
    """Creates a new faculty in the system.

    Args:
        name (str): Faculty name
        db_faculty (FacultyDAO): DAO for working with faculties
        user (User): Authorized administrator

    Returns:
        CreateFacultyResponse: Created faculty

    Raises:
        HTTPException: 403 if user is not an administrator
    """
    faculty = await db_faculty.add({"name": name})

    return CreateFacultyResponse(id=faculty.id, name=faculty.name)


@router.delete("/{faculty_id}", summary="Delete faculty")
async def delete_faculty(
    faculty_id: int,
    db_faculty: FacultyDAO = Depends(FacultyDAO),
    user: User = Depends(get_admin_user),
) -> bool:
    """Deletes a faculty from the system.

    Args:
        faculty_id (int): Unique faculty identifier
        db_faculty (FacultyDAO): DAO for working with faculties
        user (User): Authorized administrator

    Returns:
        bool: True if deletion was successful

    Raises:
        HTTPException:
            403 if user is not an administrator
            404 if faculty is not found
    """
    faculty = await db_faculty.delete(model_id=faculty_id)
    return faculty
