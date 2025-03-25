from src.crud.base import BaseDAO
from src.models import Group


class GroupDAO(BaseDAO):
    """Data Access Object (DAO) для управления пользователями в базе данных.

    Наследует базовые CRUD-операции из BaseDAO и добавляет
    специализированные методы для работы с сущностью Group.

    Примеры использования:
        group_dao = GroupDAO()
        new_group = await group_dao.add(group)

    Атрибуты:
        model (Group): SQLAlchemy модель групп, используемая для операций
    """

    model = Group
