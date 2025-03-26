from fastapi import APIRouter, Depends

from src.core.dependencies import get_admin_user, get_current_user
from src.models.enum import StatusEnum
from src.service import StudentService
from src.models import User
from src.schemas import StudentCreateRequest, StudentInfo, StudentUpdateRequest

router = APIRouter()


@router.post("", summary="Добавляет студента")
async def add_student(
    student_data: StudentCreateRequest,
    student_service: StudentService = Depends(StudentService),
    user: User = Depends(get_admin_user),
) -> StudentInfo:
    result = await student_service.add_student(student_data=student_data)
    return result


@router.get("/{id}", summary="Возвращает данные студента по ID(primary)")
async def get_student(
    student_id: int,
    student_service: StudentService = Depends(StudentService),
    user: User = Depends(get_current_user),
):
    student = await student_service.get_student_info(student_id=student_id)

    return student


@router.get("", summary="Возвращает список пользователей с фильтром")
async def get_students(
    group_id: int = None,
    enrollment_year: int = None,
    faculty_id: int = None,
    course_id: int = None,
    enrollment_status: StatusEnum = None,
    user: User = Depends(get_admin_user),
    student_service: StudentService = Depends(StudentService),
):
    result = await student_service.get_students(
        group_id=group_id,
        enrollment_year=enrollment_year,
        course_id=course_id,
        enrollment_status=enrollment_status,
        faculty_id=faculty_id,
    )
    return result


@router.put("/{id}", summary="Обновить данные студента")
async def update_student(
    student_id: int,
    update_data: StudentUpdateRequest,
    user: User = Depends(get_admin_user),
    student_service: StudentService = Depends(StudentService),
):
    result = await student_service.update_student(
        student_id=student_id, update_data=update_data
    )
    return result
