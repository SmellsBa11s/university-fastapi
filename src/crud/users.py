from src.crud.base import BaseDAO
from src.models import User


class UserDAO(BaseDAO):
    """Data Access Object (DAO) for managing users in the database.

    Inherits basic CRUD operations from BaseDAO and adds
    specialized methods for working with the User entity.

    Usage examples:
        user_dao = UserDAO()
        new_user = await user_dao.add({
                "username": "john_doe",
                "password": "secret"
            })
        found_user = await user_dao.find_one_or_none(username="john_doe")

    Attributes:
        model (User): SQLAlchemy User model used for operations
    """

    model = User
