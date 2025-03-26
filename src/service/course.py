from typing import List
from fastapi import Depends, HTTPException
from src.crud import CourseDAO
from src.models import Course, User
from src.models.enum import SemesterEnum, UserRoleEnum
from src.schemas import CreateCourseRequest, CourseInfo, UpdateCourseRequest


class CourseService:
    """Service for managing course operations in the system.

    Provides interaction with the DAO layer for performing CRUD operations with courses,
    including user access rights verification.
    """

    def __init__(self, courses_dao: CourseDAO = Depends()):
        """Initializes the service with necessary DAO objects.

        Args:
            courses_dao (CourseDAO): DAO for working with courses, injected through dependency
        """
        self._course_dao = courses_dao

    async def process_information(self, request: Course) -> CourseInfo:
        """Converts a Course object to a CourseInfo schema for API response.

        Args:
            request (Course): Course object from the database

        Returns:
            CourseInfo: Schema with course data for API response
        """
        return CourseInfo(
            id=request.id,
            title=request.title,
            description=request.description,
            course_code=request.course_code,
            credits=request.credits,
            instructor_id=request.instructor_id,
            semester=request.semester,
            year=request.year,
        )

    async def create_course(self, course_data: CreateCourseRequest) -> CourseInfo:
        """Creates a new course in the system.

        Args:
            course_data (CreateCourseRequest): Data for creating a course

        Returns:
            CourseInfo: Created course in response schema format
        """
        course = await self._course_dao.add(course_data)
        return await self.process_information(course)

    async def get_course(self, course_id: int) -> CourseInfo:
        """Gets course information by its ID.

        Args:
            course_id (int): Unique course identifier

        Returns:
            CourseInfo: Course data in response schema format

        Raises:
            HTTPException: If course is not found (404 error)
        """
        course = await self._course_dao.find_one(id=course_id)
        return await self.process_information(course)

    async def delete_course(self, course_id: int, user: User) -> bool:
        """Deletes a course from the system after access rights verification.

        Args:
            course_id (int): Unique identifier of the course to delete
            user (User): Authorized user initiating the deletion

        Returns:
            bool: True if deletion was successful

        Raises:
            HTTPException: 403 if no access rights, 404 if course is not found
        """
        course = await self._course_dao.find_one(id=course_id)
        if (user.id != course.instructor_id) and (user.user_role != UserRoleEnum.ADMIN):
            raise HTTPException(
                status_code=403, detail="You don't have permission for this"
            )
        await self._course_dao.delete(model_id=course_id)
        return True

    async def update_course(
        self, course_id: int, user: User, updated_data: UpdateCourseRequest
    ) -> CourseInfo:
        """Updates data of an existing course.

        Args:
            course_id (int): Unique identifier of the course to update
            user (User): Authorized user initiating the update
            updated_data (UpdateCourseRequest): Data to update the course

        Returns:
            CourseInfo: Updated course data in schema format

        Raises:
            HTTPException: 403 if no access rights, 404 if course is not found
        """
        update_data = updated_data.dict(exclude_none=True)

        course = await self._course_dao.find_one(id=course_id)
        if (course.instructor_id != user.id) and (user.user_role != UserRoleEnum.ADMIN):
            raise HTTPException(status_code=403, detail="You can't update this course")

        if update_data:
            course_list = await self._course_dao.update(
                model_id=course_id, **update_data
            )
            course = course_list[0]

        return await self.process_information(course)

    async def get_courses(
        self, semester: SemesterEnum = None, year: int = None, instructor_id: int = None
    ) -> List[CourseInfo]:
        """Returns a filtered list of courses.

        Args:
            semester (SemesterEnum, optional): Filter by semester
            year (int, optional): Filter by year
            instructor_id (int, optional): Filter by instructor ID

        Returns:
            List[CourseInfo]: List of courses matching the filters
        """
        course_filters = {}

        if semester is not None:
            course_filters["semester"] = semester

        if year is not None:
            course_filters["year"] = year

        if instructor_id is not None:
            course_filters["instructor_id"] = instructor_id

        courses = await self._course_dao.find_all(**course_filters)
        return [await self.process_information(course) for course in courses]
