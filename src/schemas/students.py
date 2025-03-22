from pydantic import BaseModel, Field


class StudentCreateRequest(BaseModel):
    user_id: int
    student_number: str = Field(..., max_length=20)
    group_id: int
    enrollment_year: int
    faculty_id: int


class StudentInfo(BaseModel):
    id: int
    user_id: int
    student_number: str
    group_name: str
    enrollment_year: int
    faculty_name: str


class StudentUpdateRequest(BaseModel):
    student_number: str
    group_id: int
    enrollment_year: int
    faculty_id: int
