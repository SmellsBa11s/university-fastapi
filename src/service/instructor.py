from typing import List

from fastapi import Depends

from src.crud import InstructorDAO, CourseDAO
from src.models import Instructor
from src.schemas import CreateInstructorRequest, InstructorInfo


class InstructorService:
    """Сервис для управления операциями с преподавателями с использованием DAO слоя."""

    def __init__(
        self,
        instructor_dao: InstructorDAO = Depends(),
        courses_dao: CourseDAO = Depends(),
    ):
        """Инициализирует DAO для работы с сущностями системы."""
        self._instructor_dao = instructor_dao
        self._course_dao = courses_dao

    async def process_information(self, request: Instructor) -> InstructorInfo:
        """Преобразует объект Instructor в DTO для ответа API."""
        return InstructorInfo(
            id=request.id,
            user_id=request.user_id,
            position=request.position,
            department=request.department,
            academic_degree=request.academic_degree,
        )

    async def add_instructor(
        self, instructor_data: CreateInstructorRequest
    ) -> InstructorInfo:
        """Создает нового преподавателя в системе."""
        instructor = await self._instructor_dao.add(instructor_data)
        return await self.process_information(instructor)

    async def get_instructor(self, instructor_id) -> InstructorInfo:
        """Возвращает информацию о преподавателе по его ID."""
        instructor = await self._instructor_dao.find_one(id=instructor_id)
        return await self.process_information(instructor)

    async def get_instructors(
        self, department: str = None, course_id: int = None
    ) -> List[InstructorInfo]:
        """
        Возвращает список преподавателей с фильтрацией:
        - по кафедре/отделу (department)
        - по курсу, который ведет преподаватель (course_id)
        """
        instructor_filters = {}

        if department is not None:
            instructor_filters["department"] = department

        if course_id is not None:
            course = await self._course_dao.find_one_or_none(id=course_id)
            if not course:
                return []
            instructor_filters["id"] = course.instructor_id

        instructors = await self._instructor_dao.find_all(**instructor_filters)

        return [
            await self.process_information(instructor) for instructor in instructors
        ]