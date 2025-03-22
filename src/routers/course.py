from typing import List

from fastapi import APIRouter, Depends

from src.core.dependencies import get_admin_or_instructor_user
from src.service import CourseService
from src.models import User
from src.models.enum import SemesterEnum
from src.schemas import CreateCourseRequest, CourseInfo, UpdateCourseRequest

router = APIRouter()


@router.post("", summary="Создает курс")
async def create_course(
    course_data: CreateCourseRequest,
    course_service: CourseService = Depends(CourseService),
    user: User = Depends(get_admin_or_instructor_user),
) -> CourseInfo:
    result = await course_service.create_course(course_data=course_data)
    return result


@router.get("/{id}", summary="Получить детали курса по ID")
async def get_course(
    course_id: int,
    course_service: CourseService = Depends(CourseService),
) -> CourseInfo:
    result = await course_service.get_course(course_id=course_id)
    return result


@router.get("", summary="Получить курсы с фильтрацией или без")
async def get_courses(
    semester: SemesterEnum = None,
    year: int = None,
    course_service: CourseService = Depends(CourseService),
) -> List[CourseInfo]:
    result = await course_service.get_courses(semester=semester, year=year)
    return result


@router.put("/{id}", summary="Обновить курс")
async def update_course(
    course_id: int,
    updated_data: UpdateCourseRequest,
    course_service: CourseService = Depends(CourseService),
    user: User = Depends(get_admin_or_instructor_user),
):
    result = await course_service.update_course(
        course_id=course_id, updated_data=updated_data, user=user
    )
    return result


@router.delete("/{id}", summary="Удалить курс")
async def delete_course(
    course_id: int,
    user: User = Depends(get_admin_or_instructor_user),
    course_service: CourseService = Depends(CourseService),
) -> bool:
    await course_service.delete_course(course_id=course_id, user=user)
    return True
