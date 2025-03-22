from typing import List

from fastapi import APIRouter, Depends

from src.core.dependencies import get_admin_user
from src.service import InstructorService
from src.models import User
from src.schemas import CreateInstructorRequest, InstructorInfo

router = APIRouter()


@router.post("", summary="Добавляет преподавателя")
async def add_student(
    instructor_data: CreateInstructorRequest,
    instructor_service: InstructorService = Depends(InstructorService),
    user: User = Depends(get_admin_user),
) -> InstructorInfo:
    result = await instructor_service.add_instructor(instructor_data=instructor_data)
    return result


@router.get("/{id}", summary="Получить данные преподавателя")
async def get_instructor(
    instructor_id: int,
    instructor_service: InstructorService = Depends(InstructorService),
) -> InstructorInfo:
    result = await instructor_service.get_instructor(instructor_id=instructor_id)
    return result


@router.get("", summary="Взять преподавателей по фильтрам")
async def get_instructors(
    department: str = None,
    course_id: int = None,
    instructor_service: InstructorService = Depends(InstructorService),
) -> List[InstructorInfo]:
    result = await instructor_service.get_instructors(
        department=department, course_id=course_id
    )
    return result
