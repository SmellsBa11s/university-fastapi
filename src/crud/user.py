from src.crud.base import BaseDAO
from src.models import User


class UserDAO(BaseDAO):
    """Data Access Object (DAO) для управления пользователями в базе данных.

    Наследует базовые CRUD-операции из BaseDAO и добавляет
    специализированные методы для работы с сущностью User.

    Примеры использования:
        user_dao = UserDAO()
        new_user = await user_dao.add({
                "username": "john_doe",
                "password": "secret"
            })
        found_user = await user_dao.find_one_or_none(username="john_doe")

    Атрибуты:
        model (User): SQLAlchemy модель пользователя, используемая для операций
    """

    model = User
