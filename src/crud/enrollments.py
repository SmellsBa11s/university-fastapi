from src.crud.base import BaseDAO
from src.models import Enrollment


class EnrollmentDAO(BaseDAO):
    """Data Access Object (DAO) для управления пользователями в базе данных.

    Наследует базовые CRUD-операции из BaseDAO и добавляет
    специализированные методы для работы с сущностью Enrollment.

    Примеры использования:
        enrollment_dao = EnrollmentDAO()
        new_enrollment = await enrollment_dao.add(Enrollment)

    Атрибуты:
        model (Enrollment): SQLAlchemy модель групп, используемая для операций
    """

    model = Enrollment
