from fastapi import APIRouter, Depends
from typing import List

from src.core.dependencies import get_admin_user, get_current_user
from src.models.enum import StatusEnum
from src.service import StudentService
from src.models import User
from src.schemas import StudentCreateRequest, StudentInfo, StudentUpdateRequest

router = APIRouter()


@router.post("", summary="Add student")
async def add_student(
    student_data: StudentCreateRequest,
    student_service: StudentService = Depends(StudentService),
    user: User = Depends(get_admin_user),
) -> StudentInfo:
    """Creates a new student in the system.

    Args:
        student_data (StudentCreateRequest): Data for creating a student
        student_service (StudentService): Service for working with students
        user (User): Authorized administrator

    Returns:
        StudentInfo: Created student

    Raises:
        HTTPException: 403 if user is not an administrator
    """
    result = await student_service.add_student(student_data=student_data)
    return result


@router.get("/{id}", summary="Get student data by ID")
async def get_student(
    student_id: int,
    student_service: StudentService = Depends(StudentService),
    user: User = Depends(get_current_user),
) -> StudentInfo:
    """Gets student information by their ID.

    Args:
        student_id (int): Unique student identifier
        student_service (StudentService): Service for working with students
        user (User): Authorized user

    Returns:
        StudentInfo: Student information

    Raises:
        HTTPException: 404 if student is not found
    """
    student = await student_service.get_student_info(student_id=student_id)

    return student


@router.get("", summary="Get filtered list of students")
async def get_students(
    group_id: int = None,
    enrollment_year: int = None,
    faculty_id: int = None,
    course_id: int = None,
    enrollment_status: StatusEnum = None,
    user: User = Depends(get_admin_user),
    student_service: StudentService = Depends(StudentService),
) -> List[StudentInfo]:
    """Returns a filtered list of students.

    Args:
        group_id (int, optional): Filter by group ID
        enrollment_year (int, optional): Filter by enrollment year
        faculty_id (int, optional): Filter by faculty ID
        course_id (int, optional): Filter by course ID
        enrollment_status (StatusEnum, optional): Filter by enrollment status
        user (User): Authorized administrator
        student_service (StudentService): Service for working with students

    Returns:
        List[StudentInfo]: List of students matching the filters

    Raises:
        HTTPException: 403 if user is not an administrator
    """
    result = await student_service.get_students(
        group_id=group_id,
        enrollment_year=enrollment_year,
        course_id=course_id,
        enrollment_status=enrollment_status,
        faculty_id=faculty_id,
    )
    return result


@router.put("/{id}", summary="Update student data")
async def update_student(
    student_id: int,
    update_data: StudentUpdateRequest,
    user: User = Depends(get_admin_user),
    student_service: StudentService = Depends(StudentService),
) -> StudentInfo:
    """Updates student information.

    Args:
        student_id (int): Unique student identifier
        update_data (StudentUpdateRequest): Data to update
        user (User): Authorized administrator
        student_service (StudentService): Service for working with students

    Returns:
        StudentInfo: Updated student information

    Raises:
        HTTPException:
            403 if user is not an administrator
            404 if student is not found
    """
    result = await student_service.update_student(
        student_id=student_id, update_data=update_data
    )
    return result
