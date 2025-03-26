from src.crud.base import BaseDAO
from src.models import Enrollment


class EnrollmentDAO(BaseDAO):
    """Data Access Object (DAO) for managing enrollments in the database.

    Inherits basic CRUD operations from BaseDAO and adds
    specialized methods for working with the Enrollment entity.

    Usage examples:
        enrollment_dao = EnrollmentDAO()
        new_enrollment = await enrollment_dao.add({
                "student_id": 1,
                "course_id": 1,
                "semester": "Spring",
                "grade": None
            })
        found_enrollment = await enrollment_dao.find_one_or_none(
            student_id=1, course_id=1
        )

    Attributes:
        model (Enrollment): SQLAlchemy Enrollment model used for operations
    """

    model = Enrollment
