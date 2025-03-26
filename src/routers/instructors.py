from typing import List

from fastapi import APIRouter, Depends

from src.core.dependencies import get_admin_user
from src.service import InstructorService
from src.models import User
from src.schemas import CreateInstructorRequest, InstructorInfo

router = APIRouter()


@router.post("", summary="Add instructor")
async def add_student(
    instructor_data: CreateInstructorRequest,
    instructor_service: InstructorService = Depends(InstructorService),
    user: User = Depends(get_admin_user),
) -> InstructorInfo:
    """Creates a new instructor in the system.

    Args:
        instructor_data (CreateInstructorRequest): Data for creating an instructor
        instructor_service (InstructorService): Service for working with instructors
        user (User): Authorized administrator

    Returns:
        InstructorInfo: Created instructor

    Raises:
        HTTPException: 403 if user is not an administrator
    """
    result = await instructor_service.add_instructor(instructor_data=instructor_data)
    return result


@router.get("/{id}", summary="Get instructor data")
async def get_instructor(
    instructor_id: int,
    instructor_service: InstructorService = Depends(InstructorService),
) -> InstructorInfo:
    """Gets instructor information by their ID.

    Args:
        instructor_id (int): Unique instructor identifier
        instructor_service (InstructorService): Service for working with instructors

    Returns:
        InstructorInfo: Instructor information

    Raises:
        HTTPException: 404 if instructor is not found
    """
    result = await instructor_service.get_instructor(instructor_id=instructor_id)
    return result


@router.get("", summary="Get instructors by filters")
async def get_instructors(
    department: str = None,
    course_id: int = None,
    instructor_service: InstructorService = Depends(InstructorService),
) -> List[InstructorInfo]:
    """Returns a filtered list of instructors.

    Args:
        department (str, optional): Filter by department
        course_id (int, optional): Filter by course ID that the instructor teaches
        instructor_service (InstructorService): Service for working with instructors

    Returns:
        List[InstructorInfo]: List of instructors matching the filters
    """
    result = await instructor_service.get_instructors(
        department=department, course_id=course_id
    )
    return result
