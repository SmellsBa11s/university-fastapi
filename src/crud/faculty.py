from src.crud.base import BaseDAO
from src.models import Faculty


class FacultyDAO(BaseDAO):
    """Data Access Object (DAO) for managing faculties in the database.

    Inherits basic CRUD operations from BaseDAO and adds
    specialized methods for working with the Faculty entity.

    Usage examples:
        faculty_dao = FacultyDAO()
        new_faculty = await faculty_dao.add({
                "name": "Computer Science",
                "description": "Faculty of Computer Science",
                "dean_id": 1
            })
        found_faculty = await faculty_dao.find_one_or_none(name="Computer Science")

    Attributes:
        model (Faculty): SQLAlchemy Faculty model used for operations
    """

    model = Faculty
