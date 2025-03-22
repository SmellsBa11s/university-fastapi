from pydantic import BaseModel


class InstructorInfo(BaseModel):
    id: int
    user_id: int
    position: str
    department: str
    academic_degree: str


class CreateInstructorRequest(BaseModel):
    user_id: int
    position: str
    department: str
    academic_degree: str
