from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from src.models.enum import UserRoleEnum


class UserInfo(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str
    user_role: UserRoleEnum
    created_at: datetime
    updated_at: datetime


class GetAllUsersResponse(BaseModel):
    users: List[UserInfo]


class UpdateUserRequest(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
