from pydantic import BaseModel
from src.models.enum import SemesterEnum


class CreateCourseRequest(BaseModel):
    title: str
    description: str
    course_code: str
    credits: int
    instructor_id: int
    semester: SemesterEnum
    year: int


class UpdateCourseRequest(BaseModel):
    title: str
    description: str
    course_code: str
    credits: int
    semester: SemesterEnum
    year: int


class CourseInfo(BaseModel):
    id: int
    title: str
    description: str
    course_code: str
    credits: int
    instructor_id: int
    semester: SemesterEnum
    year: int
