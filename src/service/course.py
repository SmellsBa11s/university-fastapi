from typing import List
from fastapi import Depends, HTTPException
from src.crud import CourseDAO
from src.models import Course, User
from src.models.enum import SemesterEnum, UserRoleEnum
from src.schemas import CreateCourseRequest, CourseInfo, UpdateCourseRequest


class CourseService:
    """Сервис для управления операциями с курсами в системе.

    Обеспечивает взаимодействие с DAO слоем для выполнения CRUD операций с курсами,
    включая проверку прав доступа пользователей.
    """

    def __init__(self, courses_dao: CourseDAO = Depends()):
        """Инициализирует сервис с необходимыми DAO объектами.

        Args:
            courses_dao (CourseDAO): DAO для работы с курсами, внедряется через зависимость
        """
        self._course_dao = courses_dao

    async def process_information(self, request: Course) -> CourseInfo:
        """Преобразует объект Course в схему CourseInfo для ответа API.

        Args:
            request (Course): Объект курса из базы данных

        Returns:
            CourseInfo: Схема с данными курса для возврата в API
        """
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
        """Создает новый курс в системе.

        Args:
            course_data (CreateCourseRequest): Данные для создания курса

        Returns:
            CourseInfo: Созданный курс в формате схемы для ответа
        """
        course = await self._course_dao.add(course_data)
        return await self.process_information(course)

    async def get_course(self, course_id: int) -> CourseInfo:
        """Получает информацию о курсе по его идентификатору.

        Args:
            course_id (int): Уникальный идентификатор курса

        Returns:
            CourseInfo: Данные курса в формате схемы для ответа

        Raises:
            HTTPException: Если курс не найден (404 ошибка)
        """
        course = await self._course_dao.find_one(id=course_id)
        return await self.process_information(course)

    async def delete_course(self, course_id: int, user: User) -> bool:
        """Удаляет курс из системы после проверки прав доступа.

        Args:
            course_id (int): Уникальный идентификатор курса для удаления
            user (User): Авторизованный пользователь, инициирующий удаление

        Returns:
            bool: True если удаление прошло успешно

        Raises:
            HTTPException: 403 если нет прав доступа, 404 если курс не найден
        """
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
        """Обновляет данные существующего курса.

        Args:
            course_id (int): Уникальный идентификатор обновляемого курса
            user (User): Авторизованный пользователь, инициирующий обновление
            updated_data (UpdateCourseRequest): Данные для обновления курса

        Returns:
            CourseInfo: Обновленные данные курса в формате схемы

        Raises:
            HTTPException: 403 если нет прав доступа, 404 если курс не найден
        """
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
        """Возвращает отфильтрованный список курсов.

        Args:
            semester (SemesterEnum, optional): Фильтр по семестру
            year (int, optional): Фильтр по году проведения
            instructor_id (int, optional): Фильтр по ID преподавателя

        Returns:
            List[CourseInfo]: Список курсов, соответствующих фильтрам
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
