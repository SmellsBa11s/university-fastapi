from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from src.models.base import Base

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost/university"

engine = create_async_engine(DATABASE_URL, echo=True)

async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    print("Таблицы успешно созданы!")


import asyncio

asyncio.run(init_db())
