from src.crud.base import BaseDAO
from src.models import Faculty


class FacultyDAO(BaseDAO):
    """Data Access Object (DAO) для управления пользователями в базе данных.

    Наследует базовые CRUD-операции из BaseDAO и добавляет
    специализированные методы для работы с сущностью Faculty.

    Примеры использования:
        faculty_dao = FacultyDAO()
        new_faculty = await faculty_dao.add(Faculty)

    Атрибуты:
        model (Faculty): SQLAlchemy модель групп, используемая для операций
    """

    model = Faculty
