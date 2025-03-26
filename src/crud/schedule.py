from src.crud.base import BaseDAO
from src.models import Schedule


class ScheduleDAO(BaseDAO):
    """Data Access Object (DAO) для управления пользователями в базе данных.

    Наследует базовые CRUD-операции из BaseDAO и добавляет
    специализированные методы для работы с сущностью Schedule.

    Примеры использования:
        schedule_dao = ScheduleDAO()
        new_schedule = await schedule_dao.add(Schedule)

    Атрибуты:
        model (Schedule): SQLAlchemy модель групп, используемая для операций
    """

    model = Schedule
