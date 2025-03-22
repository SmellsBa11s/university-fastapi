from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Response, Cookie
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.db.database import get_async_db
from src.crud import get_user_by_username, create_user
from src.schemas import AuthResponse, CreateUserRequest, CreateUserResponse
from src.service.auth import AuthService, pwd_context
from src.settings import settings

router = APIRouter()


@router.post("/register", summary="Register new user")
async def register_user(
    user: CreateUserRequest, db: AsyncSession = Depends(get_async_db)
) -> CreateUserResponse:
    existing_user = await get_user_by_username(username=user.username, db=db)

    if existing_user:
        raise HTTPException(status_code=400, detail="User уже зарегистрирован")

    user = await create_user(user=user, db=db)

    return CreateUserResponse(
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username,
        password=user.password,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )


@router.post("/login", summary="Login in account")
async def login(
    username: str,
    password: str,
    response: Response,
    db: AsyncSession = Depends(get_async_db),
) -> AuthResponse:
    user = await get_user_by_username(username=username, db=db)

    if not user or not pwd_context.verify(password, user.password):
        raise HTTPException(status_code=401, detail="Некорректный email или пароль")

    tokens = AuthService.generate_tokens(user)

    response.set_cookie(
        key="access_token",
        value=f"Bearer {tokens['access_token']}",
        httponly=True,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        secure=True,
        samesite="lax",
    )

    response.set_cookie(
        key="refresh_token",
        value=f"Bearer {tokens['refresh_token']}",
        httponly=True,
        max_age=settings.REFRESH_TOKEN_EXPIRE_MINUTES * 60,
        secure=True,
        samesite="lax",
    )

    return AuthResponse(**tokens)


@router.post("/refresh", summary="Refresh access token")
async def refresh_token_api(
    response: Response,
    refresh_token: Optional[str] = Cookie(default=None),
    db: AsyncSession = Depends(get_async_db),
) -> AuthResponse:
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token is missing")

    try:
        # Получаем payload из токена
        payload = AuthService.get_token_payload(refresh_token, is_refresh=True)
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid token payload")

        user = await get_user_by_username(username=username, db=db)
        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        tokens = AuthService.generate_tokens(user)

        response.set_cookie(
            key="access_token",
            value=f"Bearer {tokens['access_token']}",
            httponly=True,
            max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            secure=True,
            samesite="lax",
        )

        response.set_cookie(
            key="refresh_token",
            value=f"Bearer {tokens['refresh_token']}",
            httponly=True,
            max_age=settings.REFRESH_TOKEN_EXPIRE_MINUTES * 60,
            secure=True,
            samesite="lax",
        )

        return AuthResponse(**tokens)

    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid refresh token")


@router.post("/logout", summary="Logout into account")
async def logout(response: Response) -> None:
    response.delete_cookie(key="access")
