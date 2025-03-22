from typing import List

from fastapi import Depends, HTTPException

from src.crud import CourseDAO
from src.models import Course, User
from src.models.enum import SemesterEnum, UserRoleEnum
from src.schemas import CreateCourseRequest, CourseInfo, UpdateCourseRequest


class CourseService:
    """Сервис для управления операциями с преподавателями с использованием DAO слоя."""

    def __init__(
        self,
        courses_dao: CourseDAO = Depends(),
    ):
        """Инициализирует DAO для работы с сущностями системы."""
        self._course_dao = courses_dao

    async def process_information(self, request: Course) -> CourseInfo:
        return CourseInfo(
            id=request.id,
            title=request.title,
            description=request.description,
            course_code=request.course_code,
            credits=request.credits,
            instructor_id=request.instructor_id,
            semester=request.semester,
            year=request.year,
        )

    async def create_course(self, course_data: CreateCourseRequest) -> CourseInfo:
        course = await self._course_dao.add(course_data)
        return await self.process_information(course)

    async def get_course(self, course_id: int) -> CourseInfo:
        course = await self._course_dao.find_one(id=course_id)
        return await self.process_information(course)

    async def delete_course(self, course_id: int, user: User) -> bool:
        course = await self._course_dao.find_one(id=course_id)
        if (user.id != course.instructor_id) and (user.user_role != UserRoleEnum.ADMIN):
            raise HTTPException(
                status_code=403, detail="You don't have permission for this"
            )
        await self._course_dao.delete(model_id=course_id)
        return True

    async def update_course(
        self, course_id: int, user: User, updated_data: UpdateCourseRequest
    ) -> CourseInfo:
        update_data = updated_data.dict(exclude_none=True)

        course = await self._course_dao.find_one(id=course_id)
        if (course.instructor_id != user.id) and (user.user_role != UserRoleEnum.ADMIN):
            raise HTTPException(status_code=403, detail="You can't update this course")

        if update_data:
            course_list = await self._course_dao.update(
                model_id=course_id, **update_data
            )
            course = course_list[0]

        return await self.process_information(course)

    async def get_courses(
        self, semester: SemesterEnum = None, year: int = None, instructor_id: int = None
    ) -> List[CourseInfo]:
        """
        Возвращает список курсов с возможностью фильтрации:
        - по семестру
        - по учебному году
        - по преподавателю

        Args:
            semester (SemesterEnum, optional): Фильтр по семестру
            year (int, optional): Фильтр по учебному году
            instructor_id (int, optional): Фильтр по ID преподавателя

        Returns:
            List[Course]: Список объектов Course, удовлетворяющих фильтрам
        """
        course_filters = {}

        if semester is not None:
            course_filters["semester"] = semester

        if year is not None:
            course_filters["year"] = year

        if instructor_id is not None:
            course_filters["instructor_id"] = instructor_id
        courses = await self._course_dao.find_all(**course_filters)
        return [await self.process_information(course) for course in courses]
