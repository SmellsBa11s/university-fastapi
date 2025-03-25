from datetime import datetime, timedelta

from fastapi import HTTPException
from passlib.context import CryptContext
import jwt
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

    @staticmethod
    def verify_refresh_token(token: str) -> dict:
        try:
            payload = jwt.decode(
                token, settings.REFRESH_SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            return payload
        except:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

    @staticmethod
    def verify_access_token(token: str) -> dict:
        try:
            payload = jwt.decode(
                token, settings.ACCESS_SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            return payload
        except:
            raise HTTPException(status_code=401, detail="Invalid access token")

    @classmethod
    def get_token_payload(cls, token: str, is_refresh: bool = False) -> dict:
        token = token.replace("Bearer ", "")
        try:
            if is_refresh:
                return cls.verify_refresh_token(token)
            return cls.verify_access_token(token)
        except HTTPException:
            raise
