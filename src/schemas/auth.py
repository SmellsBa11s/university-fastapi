from datetime import datetime

from pydantic import BaseModel

from src.models.enum import UserRoleEnum


class AuthResponse(BaseModel):
    access_token: str
    refresh_token: str


class CreateUserRequest(BaseModel):
    first_name: str
    last_name: str
    username: str
    password: str


class CreateUserResponse(BaseModel):
    first_name: str
    last_name: str
    username: str
    password: str
    user_role: UserRoleEnum
    created_at: datetime
    updated_at: datetime
