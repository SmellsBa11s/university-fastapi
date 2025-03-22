import jwt
from fastapi import Depends, HTTPException
from fastapi import Cookie

from src.crud.users import UserDAO
from src.models import User
from src.models.enum import UserRoleEnum
from src.settings import settings


async def get_current_user(
    access_token: str = Cookie(None),
    db_user: UserDAO = Depends()
) -> User:
    """Получает аутентифицированного пользователя на основе JWT токена.

    Извлекает access token из куки, проверяет его валидность и возвращает
    соответствующего пользователя из базы данных.

    Args:
        access_token (str, optional): JWT токен из cookie. Defaults to None.
        db_user (UserDAO): DAO для работы с пользователями (внедряется через зависимость)

    Returns:
        User: Объект аутентифицированного пользователя

    Raises:
        HTTPException:
            401 - Если токен отсутствует или невалиден
            403 - Если пользователь деактивирован
    """
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


async def get_admin_user(user: User = Depends(get_current_user)) -> User:
    """Проверяет права доступа для администратора.

    Должен использоваться как зависимость в эндпоинтах, требующих прав администратора.

    Args:
        user (User): Аутентифицированный пользователь (из зависимости get_current_user)

    Returns:
        User: Объект пользователя с ролью ADMIN

    Raises:
        HTTPException:
            403 - Если у пользователя нет прав администратора
    """
    if user.user_role != UserRoleEnum.ADMIN:
        raise HTTPException(status_code=403, detail="Only admin can do this")

    return user


async def get_admin_or_instructor_user(user: User = Depends(get_current_user)) -> User:
    """Проверяет права доступа для администратора или инструктора.

    Должен использоваться как зависимость в эндпоинтах, требующих прав
    администратора или инструктора.

    Args:
        user (User): Аутентифицированный пользователь (из зависимости get_current_user)

    Returns:
        User: Объект пользователя с ролью ADMIN или INSTRUCTOR

    Raises:
        HTTPException:
            403 - Если у пользователя нет требуемых прав
    """
    if (user.user_role != UserRoleEnum.ADMIN) and (
        user.user_role != UserRoleEnum.INSTRUCTOR
    ):
        raise HTTPException(
            status_code=403, detail="Only admin or instructor can do this"
        )
    return user