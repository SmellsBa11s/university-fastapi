from pydantic import BaseModel


class CreateFacultyResponse(BaseModel):
    id: int
    name: str
