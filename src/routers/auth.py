from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.db.database import get_async_db
from src.crud import get_user_by_username, create_user
from src.schemas import AuthResponse, UserBase
from src.service.auth import AuthService, pwd_context
from src.settings import settings

router = APIRouter()


@router.post("/register", summary="Register new user")
async def register_user(
    user: UserBase, db: AsyncSession = Depends(get_async_db)
) -> UserBase:
    existing_user = await get_user_by_username(username=user.username, db=db)

    if existing_user:
        raise HTTPException(status_code=400, detail="User уже зарегистрирован")

    user = await create_user(user=user, db=db)

    return UserBase(username=user.username, password=user.password)


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


@router.post("/logout", summary="Logout into account")
async def logout(response: Response) -> None:
    response.delete_cookie(key="access")
