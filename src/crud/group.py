from src.crud.base import BaseDAO
from src.models import Group


class GroupDAO(BaseDAO):
    """Data Access Object (DAO) for managing groups in the database.

    Inherits basic CRUD operations from BaseDAO and adds
    specialized methods for working with the Group entity.

    Usage examples:
        group_dao = GroupDAO()
        new_group = await group_dao.add({
                "name": "Group A",
                "faculty_id": 1
            })
        found_group = await group_dao.find_one_or_none(name="Group A")

    Attributes:
        model (Group): SQLAlchemy Group model used for operations
    """

    model = Group
