from typing import List
from fastapi import Depends

from src.crud import StudentDAO, FacultyDAO, GroupDAO, CourseDAO, EnrollmentDAO, UserDAO
from src.models.enum import StatusEnum, UserRoleEnum
from src.schemas import StudentCreateRequest, StudentInfo, StudentUpdateRequest


class StudentService:
    """Service for managing student operations using the DAO layer.

    Provides a complete cycle of working with student data: creation, updating,
    retrieving information and complex filtering with related entities.
    """

    def __init__(
        self,
        user_dao: UserDAO = Depends(),
        student_dao: StudentDAO = Depends(),
        faculty_dao: FacultyDAO = Depends(),
        group_dao: GroupDAO = Depends(),
        enrollment_dao: EnrollmentDAO = Depends(),
        courses_dao: CourseDAO = Depends(),
    ):
        """Initializes DAO for working with system entities.

        Args:
            user_dao (UserDAO): DAO for working with users
            student_dao (StudentDAO): DAO for working with students
            faculty_dao (FacultyDAO): DAO for working with faculties
            group_dao (GroupDAO): DAO for working with groups
            enrollment_dao (EnrollmentDAO): DAO for working with course enrollments
            courses_dao (CourseDAO): DAO for working with courses
        """
        self._user_dao = user_dao
        self._student_dao = student_dao
        self._faculty_dao = faculty_dao
        self._group_dao = group_dao
        self._enrollment_dao = enrollment_dao
        self._course_dao = courses_dao

    async def get_student_info(self, student_id: int) -> StudentInfo:
        """Gets extended information about a student by their ID.

        Args:
            student_id (int): Unique student identifier

        Returns:
            StudentInfo: DTO with complete student information including group and faculty

        Raises:
            HTTPException: 404 if student or related entities are not found
        """
        student_data = await self._student_dao.find_one(id=student_id)
        group = await self._group_dao.find_one(id=student_data.group_id)
        faculty = await self._faculty_dao.find_one(id=student_data.faculty_id)

        return StudentInfo(
            id=student_data.id,
            user_id=student_data.user_id,
            student_number=student_data.student_number,
            group_name=group.name,
            enrollment_year=student_data.enrollment_year,
            faculty_name=faculty.name,
        )

    async def add_student(self, student_data: StudentCreateRequest) -> StudentInfo:
        """Creates a new student and returns their extended data.

        Args:
            student_data (StudentCreateRequest): DTO with data for student creation

        Returns:
            StudentInfo: Created student with complete information

        Raises:
            HTTPException:
                400 - On data validation errors
                404 - If related group or faculty does not exist
        """
        student = await self._student_dao.add(student_data)
        await self._user_dao.update(
            model_id=student.user_id, user_role=UserRoleEnum.STUDENT
        )
        return await self.get_student_info(student.id)

    async def get_students(
        self,
        group_id: int = None,
        enrollment_year: int = None,
        faculty_id: int = None,
        course_id: int = None,
        enrollment_status: StatusEnum = None,
    ) -> List[StudentInfo]:
        """Returns a filtered list of students with additional information.

        Supports combined filtering by:
        - Group
        - Enrollment year
        - Faculty
        - Course (through course enrollments)
        - Course enrollment status

        Args:
            group_id (int, optional): Filter by group ID
            enrollment_year (int, optional): Filter by enrollment year
            faculty_id (int, optional): Filter by faculty ID
            course_id (int, optional): Filter by course ID
            enrollment_status (StatusEnum, optional): Filter by enrollment status

        Returns:
            List[StudentInfo]: List of students matching the filters
        """
        student_filters = {}

        if group_id is not None:
            student_filters["group_id"] = group_id

        if enrollment_year is not None:
            student_filters["enrollment_year"] = enrollment_year

        if faculty_id is not None:
            student_filters["faculty_id"] = faculty_id

        students = await self._student_dao.find_all(**student_filters)

        if course_id is not None or enrollment_status is not None:
            enrollment_filter = {}
            if course_id is not None:
                enrollment_filter["course_id"] = course_id
            if enrollment_status is not None:
                enrollment_filter["status"] = enrollment_status

            enrollments = await self._enrollment_dao.find_all(**enrollment_filter)
            valid_student_ids = {e.student_id for e in enrollments}
            students = [s for s in students if s.id in valid_student_ids]

        return [await self.get_student_info(student.id) for student in students]

    async def update_student(self, student_id: int, update_data: StudentUpdateRequest):
        """Updates student data and returns current information.

        Args:
            student_id (int): ID of the student to update
            update_data (StudentUpdateRequest): DTO with fields to update

        Returns:
            StudentInfo: Updated student data

        Raises:
            HTTPException:
                404 - If student is not found
                400 - On data validation errors
        """
        update_data = update_data.dict(exclude_none=True)

        if update_data:
            student_list = await self._student_dao.update(
                model_id=student_id, **update_data
            )
            student = student_list[0]
        else:
            student = await self._student_dao.find_one(id=student_id)

        return await self.get_student_info(student_id=student.id)
