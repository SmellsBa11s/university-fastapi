from fastapi import Depends, HTTPException
import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Cookie

from src.core.db.database import get_async_db
from src.crud.user import get_user_by_username
from src.settings import settings


async def get_current_user(
    access_token: str = Cookie(None), db: AsyncSession = Depends(get_async_db)
):
    if not access_token:
        raise HTTPException(status_code=401, detail="Токен отсутствует")

    token = access_token.replace("Bearer ", "")

    payload = jwt.decode(
        token, settings.ACCESS_SECRET_KEY, algorithms=[settings.ALGORITHM]
    )

    username: str = payload.get("sub")
    if username is None:
        raise HTTPException(status_code=401, detail="Неверный токен")

    user = await get_user_by_username(username=username, db=db)
    if user is None:
        raise HTTPException(status_code=401, detail="Пользователь не найден")
    return user
