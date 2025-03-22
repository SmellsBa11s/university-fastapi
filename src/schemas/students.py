from pydantic import BaseModel


class StudentCreateRequest(BaseModel):
    user_id: int
    student_number: str  # добавить длину 20
    group_id: int
    enrollment_year: int
    faculty_id: int
