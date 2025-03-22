from src.crud.base import BaseDAO
from src.models import Student


class StudentDAO(BaseDAO):
    """Data Access Object (DAO) для управления пользователями в базе данных.

    Наследует базовые CRUD-операции из BaseDAO и добавляет
    специализированные методы для работы с сущностью Student.

    Примеры использования:
        student_dao = StudentDAO()
        new_student = await student_dao.add(Student)

    Атрибуты:
        model (Student): SQLAlchemy модель групп, используемая для операций
    """

    model = Student
