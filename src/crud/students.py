from src.crud.base import BaseDAO
from src.models import Student


class StudentDAO(BaseDAO):
    """Data Access Object (DAO) for managing students in the database.

    Inherits basic CRUD operations from BaseDAO and adds
    specialized methods for working with the Student entity.

    Usage examples:
        student_dao = StudentDAO()
        new_student = await student_dao.add({
                "user_id": 1,
                "group_id": 1,
                "student_id": "2"
            })
        found_student = await student_dao.find_one_or_none(student_id="2024001")

    Attributes:
        model (Student): SQLAlchemy Student model used for operations
    """

    model = Student
