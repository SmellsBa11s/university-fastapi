from src.crud.base import BaseDAO
from src.models import Instructor


class InstructorDAO(BaseDAO):
    """Data Access Object (DAO) for managing instructors in the database.

    Inherits basic CRUD operations from BaseDAO and adds
    specialized methods for working with the Instructor entity.

    Usage examples:
        instructor_dao = InstructorDAO()
        new_instructor = await instructor_dao.add({
                "user_id": 1,
                "department": "Computer Science",
                "position": "Associate Professor"
            })
        found_instructor = await instructor_dao.find_one_or_none(user_id=1)

    Attributes:
        model (Instructor): SQLAlchemy Instructor model used for operations
    """

    model = Instructor
