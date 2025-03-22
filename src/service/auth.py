from datetime import datetime, timedelta

from jose import JWTError
from passlib.context import CryptContext
import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud import get_user_by_username
from src.models import User
from src.settings import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire})
        return jwt.encode(
            to_encode, settings.ACCESS_SECRET_KEY, algorithm=settings.ALGORITHM
        )

    @staticmethod
    def create_refresh_token(data: dict, expires_delta: timedelta) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire})
        return jwt.encode(
            to_encode, settings.REFRESH_SECRET_KEY, algorithm=settings.ALGORITHM
        )

    @classmethod
    def generate_tokens(cls, user: User) -> dict:
        token_data = {
            "sub": user.username,
        }

        return {
            "access_token": cls.create_access_token(
                data=token_data,
                expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
            ),
            "refresh_token": cls.create_refresh_token(
                data=token_data,
                expires_delta=timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES),
            ),
        }
