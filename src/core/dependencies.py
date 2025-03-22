import jwt
from fastapi import Depends, HTTPException
from fastapi import Cookie

from src.crud.users import UserDAO
from src.settings import settings


async def get_current_user(
    access_token: str = Cookie(None), db_user: UserDAO = Depends()
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

    user = await db_user.find_one(username=username)
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Пользователь деактивирован")
    return user
