from typing import List
from fastapi import Depends

from src.crud import StudentDAO, FacultyDAO, GroupDAO, CourseDAO, EnrollmentDAO, UserDAO
from src.models.enum import StatusEnum, UserRoleEnum
from src.schemas import StudentCreateRequest, StudentInfo, StudentUpdateRequest


class StudentService:
    """Сервис для управления операциями со студентами с использованием DAO слоя.

    Обеспечивает полный цикл работы с данными студентов: создание, обновление,
    получение информации и комплексную фильтрацию с учетом связанных сущностей.
    """

    def __init__(
            self,
            user_dao: UserDAO = Depends(),
            student_dao: StudentDAO = Depends(),
            faculty_dao: FacultyDAO = Depends(),
            group_dao: GroupDAO = Depends(),
            enrollment_dao: EnrollmentDAO = Depends(),
            courses_dao: CourseDAO = Depends(),
    ):
        """Инициализирует DAO для работы с сущностями системы.

        Args:
            user_dao (UserDAO): DAO для работы с пользователями
            student_dao (StudentDAO): DAO для работы со студентами
            faculty_dao (FacultyDAO): DAO для работы с факультетами
            group_dao (GroupDAO): DAO для работы с группами
            enrollment_dao (EnrollmentDAO): DAO для работы с записями на курсы
            courses_dao (CourseDAO): DAO для работы с курсами
        """
        self._user_dao = user_dao
        self._student_dao = student_dao
        self._faculty_dao = faculty_dao
        self._group_dao = group_dao
        self._enrollment_dao = enrollment_dao
        self._course_dao = courses_dao

    async def get_student_info(self, student_id: int) -> StudentInfo:
        """Получает расширенную информацию о студенте по его идентификатору.

        Args:
            student_id (int): Уникальный идентификатор студента

        Returns:
            StudentInfo: DTO с полной информацией о студенте включая группу и факультет

        Raises:
            HTTPException: 404 если студент или связанные сущности не найдены
        """
        student_data = await self._student_dao.find_one(id=student_id)
        group = await self._group_dao.find_one(id=student_data.group_id)
        faculty = await self._faculty_dao.find_one(id=student_data.faculty_id)

        return StudentInfo(
            id=student_data.id,
            user_id=student_data.user_id,
            student_number=student_data.student_number,
            group_name=group.name,
            enrollment_year=student_data.enrollment_year,
            faculty_name=faculty.name,
        )

    async def add_student(self, student_data: StudentCreateRequest) -> StudentInfo:
        """Создает нового студента и возвращает его расширенные данные.

        Args:
            student_data (StudentCreateRequest): DTO с данными для создания студента

        Returns:
            StudentInfo: Созданный студент с полной информацией

        Raises:
            HTTPException:
                400 - При ошибках валидации данных
                404 - Если связанная группа или факультет не существуют
        """
        student = await self._student_dao.add(student_data)
        await self._user_dao.update(
            model_id=student.user_id, user_role=UserRoleEnum.STUDENT
        )
        return await self.get_student_info(student.id)

    async def get_students(
            self,
            group_id: int = None,
            enrollment_year: int = None,
            faculty_id: int = None,
            course_id: int = None,
            enrollment_status: StatusEnum = None,
    ) -> List[StudentInfo]:
        """Возвращает отфильтрованный список студентов с дополнительной информацией.

        Поддерживает комбинированную фильтрацию по:
        - Группе
        - Году поступления
        - Факультету
        - Курсу (через записи на курсы)
        - Статусу записи на курс

        Args:
            group_id (int, optional): Фильтр по ID группы
            enrollment_year (int, optional): Фильтр по году поступления
            faculty_id (int, optional): Фильтр по ID факультета
            course_id (int, optional): Фильтр по ID курса
            enrollment_status (StatusEnum, optional): Фильтр по статусу записи

        Returns:
            List[StudentInfo]: Список студентов, соответствующих фильтрам
        """
        student_filters = {}

        if group_id is not None:
            student_filters["group_id"] = group_id

        if enrollment_year is not None:
            student_filters["enrollment_year"] = enrollment_year

        if faculty_id is not None:
            student_filters["faculty_id"] = faculty_id

        students = await self._student_dao.find_all(**student_filters)

        if course_id is not None or enrollment_status is not None:
            enrollment_filter = {}
            if course_id is not None:
                enrollment_filter["course_id"] = course_id
            if enrollment_status is not None:
                enrollment_filter["status"] = enrollment_status

            enrollments = await self._enrollment_dao.find_all(**enrollment_filter)
            valid_student_ids = {e.student_id for e in enrollments}
            students = [s for s in students if s.id in valid_student_ids]

        return [await self.get_student_info(student.id) for student in students]

    async def update_student(self, student_id: int, update_data: StudentUpdateRequest):
        """Обновляет данные студента и возвращает актуальную информацию.

        Args:
            student_id (int): ID обновляемого студента
            update_data (StudentUpdateRequest): DTO с обновляемыми полями

        Returns:
            StudentInfo: Обновленные данные студента

        Raises:
            HTTPException:
                404 - Если студент не найден
                400 - При ошибках валидации данных
        """
        update_data = update_data.dict(exclude_none=True)

        if update_data:
            student_list = await self._student_dao.update(
                model_id=student_id, **update_data
            )
            student = student_list[0]
        else:
            student = await self._student_dao.find_one(id=student_id)

        return await self.get_student_info(student_id=student.id)