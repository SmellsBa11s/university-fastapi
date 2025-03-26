from datetime import datetime, timedelta

from fastapi import HTTPException
from passlib.context import CryptContext
import jwt
from src.models import User
from src.settings import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    """Service for working with authentication and tokens."""

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta) -> str:
        """Creates a JWT access token with specified lifetime."""
        to_encode = data.copy()
        expire = datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire})
        return jwt.encode(
            to_encode, settings.ACCESS_SECRET_KEY, algorithm=settings.ALGORITHM
        )

    @staticmethod
    def create_refresh_token(data: dict, expires_delta: timedelta) -> str:
        """Creates a JWT refresh token with specified lifetime."""
        to_encode = data.copy()
        expire = datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire})
        return jwt.encode(
            to_encode, settings.REFRESH_SECRET_KEY, algorithm=settings.ALGORITHM
        )

    @classmethod
    def generate_tokens(cls, user: User) -> dict:
        """Generates a pair of access and refresh tokens for a user."""
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
        """Verifies the validity of a refresh token and returns its payload."""
        try:
            payload = jwt.decode(
                token, settings.REFRESH_SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            return payload
        except:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

    @staticmethod
    def verify_access_token(token: str) -> dict:
        """Verifies the validity of an access token and returns its payload."""
        try:
            payload = jwt.decode(
                token, settings.ACCESS_SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            return payload
        except:
            raise HTTPException(status_code=401, detail="Invalid access token")

    @classmethod
    def get_token_payload(cls, token: str, is_refresh: bool = False) -> dict:
        """Extracts and verifies payload from a token (access or refresh)."""
        token = token.replace("Bearer ", "")
        try:
            if is_refresh:
                return cls.verify_refresh_token(token)
            return cls.verify_access_token(token)
        except HTTPException:
            raise
