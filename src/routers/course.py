from typing import List

from fastapi import APIRouter, Depends

from src.core.dependencies import get_admin_or_instructor_user
from src.service import CourseService
from src.models import User
from src.models.enum import SemesterEnum
from src.schemas import CreateCourseRequest, CourseInfo, UpdateCourseRequest

router = APIRouter()


@router.post("", summary="Create course")
async def create_course(
    course_data: CreateCourseRequest,
    course_service: CourseService = Depends(CourseService),
    user: User = Depends(get_admin_or_instructor_user),
) -> CourseInfo:
    """Creates a new course in the system.

    Args:
        course_data (CreateCourseRequest): Data for creating a course
        course_service (CourseService): Service for working with courses
        user (User): Authorized administrator or instructor

    Returns:
        CourseInfo: Created course

    Raises:
        HTTPException: 403 if user does not have permission to create a course
    """
    result = await course_service.create_course(course_data=course_data)
    return result


@router.get("/{id}", summary="Get course details by ID")
async def get_course(
    course_id: int,
    course_service: CourseService = Depends(CourseService),
) -> CourseInfo:
    """Gets course information by its ID.

    Args:
        course_id (int): Unique course identifier
        course_service (CourseService): Service for working with courses

    Returns:
        CourseInfo: Course information

    Raises:
        HTTPException: 404 if course is not found
    """
    result = await course_service.get_course(course_id=course_id)
    return result


@router.get("", summary="Get filtered courses")
async def get_courses(
    semester: SemesterEnum = None,
    year: int = None,
    course_service: CourseService = Depends(CourseService),
) -> List[CourseInfo]:
    """Returns a filtered list of courses.

    Args:
        semester (SemesterEnum, optional): Filter by semester
        year (int, optional): Filter by year
        course_service (CourseService): Service for working with courses

    Returns:
        List[CourseInfo]: List of courses matching the filters
    """
    result = await course_service.get_courses(semester=semester, year=year)
    return result


@router.put("/{id}", summary="Update course")
async def update_course(
    course_id: int,
    updated_data: UpdateCourseRequest,
    course_service: CourseService = Depends(CourseService),
    user: User = Depends(get_admin_or_instructor_user),
) -> CourseInfo:
    """Updates course information.

    Args:
        course_id (int): Unique course identifier
        updated_data (UpdateCourseRequest): Data to update
        course_service (CourseService): Service for working with courses
        user (User): Authorized administrator or course instructor

    Returns:
        CourseInfo: Updated course information

    Raises:
        HTTPException:
            403 if user does not have permission to update the course
            404 if course is not found
    """
    result = await course_service.update_course(
        course_id=course_id, updated_data=updated_data, user=user
    )
    return result


@router.delete("/{id}", summary="Delete course")
async def delete_course(
    course_id: int,
    user: User = Depends(get_admin_or_instructor_user),
    course_service: CourseService = Depends(CourseService),
) -> bool:
    """Deletes a course from the system.

    Args:
        course_id (int): Unique course identifier
        user (User): Authorized administrator or course instructor
        course_service (CourseService): Service for working with courses

    Returns:
        bool: True if deletion was successful

    Raises:
        HTTPException:
            403 if user does not have permission to delete the course
            404 if course is not found
    """
    await course_service.delete_course(course_id=course_id, user=user)
    return True
