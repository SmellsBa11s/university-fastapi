from src.crud.base import BaseDAO
from src.models import Course


class CourseDAO(BaseDAO):
    """Data Access Object (DAO) для управления пользователями в базе данных.

    Наследует базовые CRUD-операции из BaseDAO и добавляет
    специализированные методы для работы с сущностью Course.

    Примеры использования:
        course_dao = CourseDAO()
        new_course = await course_dao.add(Course)

    Атрибуты:
        model (Course): SQLAlchemy модель групп, используемая для операций
    """

    model = Course
