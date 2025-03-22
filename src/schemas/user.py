from pydantic import BaseModel


class AuthResponse(BaseModel):
    access_token: str
    refresh_token: str


class UserBase(BaseModel):
    username: str
    password: str
