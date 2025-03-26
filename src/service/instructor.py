from typing import List

from fastapi import Depends

from src.crud import InstructorDAO, CourseDAO, UserDAO
from src.models import Instructor
from src.models.enum import UserRoleEnum
from src.schemas import CreateInstructorRequest, InstructorInfo


class InstructorService:
    """Service for managing instructor operations.

    Provides interaction with the DAO layer for performing CRUD operations with instructors,
    including managing related courses and user roles.
    """

    def __init__(
        self,
        user_dao: UserDAO = Depends(),
        instructor_dao: InstructorDAO = Depends(),
        courses_dao: CourseDAO = Depends(),
    ):
        """Initializes the service with necessary DAO objects.

        Args:
            user_dao (UserDAO): DAO for working with users
            instructor_dao (InstructorDAO): DAO for working with instructors
            courses_dao (CourseDAO): DAO for working with courses
        """
        self._user_dao = user_dao
        self._instructor_dao = instructor_dao
        self._course_dao = courses_dao

    async def process_information(self, request: Instructor) -> InstructorInfo:
        """Converts an Instructor object to an InstructorInfo schema for API response.

        Args:
            request (Instructor): Instructor object from the database

        Returns:
            InstructorInfo: Schema with instructor data for API response
        """
        return InstructorInfo(
            id=request.id,
            user_id=request.user_id,
            position=request.position,
            department=request.department,
            academic_degree=request.academic_degree,
        )

    async def add_instructor(
        self, instructor_data: CreateInstructorRequest
    ) -> InstructorInfo:
        """Creates a new instructor in the system.

        Args:
            instructor_data (CreateInstructorRequest): Data for creating an instructor

        Returns:
            InstructorInfo: Created instructor in response schema format

        Raises:
            HTTPException: 400 on data validation errors
        """
        instructor = await self._instructor_dao.add(instructor_data)
        await self._user_dao.update(
            model_id=instructor.user_id, user_role=UserRoleEnum.INSTRUCTOR
        )
        return await self.process_information(instructor)

    async def get_instructor(self, instructor_id) -> InstructorInfo:
        """Gets instructor information by their ID.

        Args:
            instructor_id (int): Unique instructor identifier

        Returns:
            InstructorInfo: Instructor data in response schema format

        Raises:
            HTTPException: 404 if instructor is not found
        """
        instructor = await self._instructor_dao.find_one(id=instructor_id)
        return await self.process_information(instructor)

    async def get_instructors(
        self, department: str = None, course_id: int = None
    ) -> List[InstructorInfo]:
        """Returns a filtered list of instructors.

        Args:
            department (str, optional): Filter by department
            course_id (int, optional): Filter by course ID that the instructor teaches

        Returns:
            List[InstructorInfo]: List of instructors matching the filters
        """
        instructor_filters = {}

        if department is not None:
            instructor_filters["department"] = department

        if course_id is not None:
            course = await self._course_dao.find_one_or_none(id=course_id)
            if not course:
                return []
            instructor_filters["id"] = course.instructor_id

        instructors = await self._instructor_dao.find_all(**instructor_filters)

        return [
            await self.process_information(instructor) for instructor in instructors
        ]
