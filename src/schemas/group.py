from pydantic import BaseModel


class CreateGroupResponse(BaseModel):
    id: int
    name: str
