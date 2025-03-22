from src.crud.base import BaseDAO
from src.models import Instructor


class InstructorDAO(BaseDAO):
    """Data Access Object (DAO) для управления пользователями в базе данных.

    Наследует базовые CRUD-операции из BaseDAO и добавляет
    специализированные методы для работы с сущностью Instructor.

    Примеры использования:
        instructor_dao = InstructorDAO()
        new_instructor = await instructor_dao.add(Instructor)

    Атрибуты:
        model (Instructor): SQLAlchemy модель групп, используемая для операций
    """

    model = Instructor
