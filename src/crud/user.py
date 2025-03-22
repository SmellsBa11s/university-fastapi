from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.core.db.database import get_async_db
from src.models import User
from src.schemas import UserBase
from src.service.auth import pwd_context


async def get_user_by_username(
    username: str, db: AsyncSession = Depends(get_async_db)
) -> User:
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalars().first()
    return user


async def get_user_by_id(
    user_id: int, db: AsyncSession = Depends(get_async_db)
) -> User:
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    return user


async def create_user(user: UserBase, db: AsyncSession = Depends(get_async_db)) -> User:
    hashed_password = pwd_context.hash(user.password)
    db_user = User(
        username=user.username,
        password=hashed_password,
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user
