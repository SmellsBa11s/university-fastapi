from src.crud.base import BaseDAO
from src.models import Course


class CourseDAO(BaseDAO):
    """Data Access Object (DAO) for managing courses in the database.

    Inherits basic CRUD operations from BaseDAO and adds
    specialized methods for working with the Course entity.

    Usage examples:
        course_dao = CourseDAO()
        new_course = await course_dao.add({
                "name": "Introduction to Programming",
                "description": "Basic programming concepts",
                "credits": 3,
                "instructor_id": 1
            })
        found_course = await course_dao.find_one_or_none(name="Introduction to Programming")

    Attributes:
        model (Course): SQLAlchemy Course model used for operations
    """

    model = Course
