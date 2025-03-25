from fastapi import Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import insert, delete, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.core.db.database import get_async_db


class BaseDAO:
    """Абстрактный Data Access Object (DAO) с базовыми CRUD-операциями.

    Требует установки атрибута `model` в дочерних классах.
    Автоматически управляет сессиями через внедрение зависимостей.

    Атрибуты:
        model (DeclarativeBase): SQLAlchemy модель для операций
    """

    model = None

    def __init__(self, session: AsyncSession = Depends(get_async_db)):
        """Инициализирует DAO сессией базы данных.

        Аргументы:
            session (AsyncSession): Асинхронная сессия SQLAlchemy,
                внедряемая через FastAPI Depends
        """
        self.session = session

    async def add(self, data: dict | BaseModel):
        """Создает новую запись в базе данных.

        Аргументы:
            data (dict | BaseModel): Словарь или Pydantic-модель
                с данными для создания

        Возвращает:
            model: Созданный экземпляр модели

        Исключения:
            ValueError: При пустых или невалидных данных
            SQLAlchemyError: При ошибках работы с базой данных
        """
        try:
            if isinstance(data, BaseModel):
                data = data.model_dump()

            query = insert(self.model).values(**data).returning(self.model)
            result = await self.session.execute(query)
            await self.session.commit()
            return result.scalar_one()
        except Exception as e:
            await self.session.rollback()
            raise HTTPException(status_code=409, detail=f"Ошибка базы данных: {str(e)}")

    async def find_one(self, **filter_by):
        """Ищет одну запись по заданным фильтрам.

        Аргументы:
            **filter_by: Аргументы для условия WHERE
                (пример: username="john")

        Возвращает:
            model Найденный объект модели
        """
        query = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(query)
        result = res.scalar_one_or_none()
        if not result:
            raise HTTPException(
                status_code=404,
                detail=f"{self.model.__name__} with filter {filter_by} not found",
            )
        return result

    async def find_one_or_none(self, **filter_by):
        """Ищет одну запись по заданным фильтрам.

        Аргументы:
            **filter_by: Аргументы для условия WHERE
                (пример: username="john")

        Возвращает:
            model Найденный объект модели или None если не найдена(для частных случаев)
        """
        query = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(query)
        return res.scalar_one_or_none()

    async def find_all(self, **filter_by):
        """Ищет все записи по заданным фильтрам.

        Аргументы:
            **filter_by: Аргументы для условия WHERE
                (пример: is_active=True)

        Возвращает:
            list[model]: Список найденных объектов модели
        """
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def delete(self, model_id: int):
        """Удаляет запись по идентификатору.

        Аргументы:
            model_id (int): ID записи для удаления

        Возвращает:
            bool | None: True при успешном удалении,
                None если запись не найдена
        """
        query = select(self.model).filter_by(id=model_id)
        result = await self.session.execute(query)
        if not result.scalar_one_or_none():
            raise HTTPException(
                status_code=404,
                detail=f"{self.model.__name__} with id {model_id} not found",
            )
        stmt = delete(self.model).where(self.model.id == model_id)
        await self.session.execute(stmt)
        await self.session.commit()

        return True

    async def update(self, model_id: int, **update_data):
        """Обновляет запись по идентификатору.

        Аргументы:
            model_id (int): ID записи для обновления
            **update_data: Данные для обновления
                (пример: username="new_name")

        Возвращает:
            model | None: Обновленный объект модели
                или None если запись не найдена
        """
        try:
            query = select(self.model).filter_by(id=model_id)
            result = await self.session.execute(query)
            if not result.scalar_one_or_none():
                raise HTTPException(
                    status_code=404,
                    detail=f"{self.model.__name__} with id {model_id} not found",
                )

            stmt = (
                update(self.model)
                .where(self.model.id == model_id)
                .values(**update_data)
                .returning(self.model)
            )
            result = await self.session.execute(stmt)
            await self.session.commit()

            return result.scalars().all()

        except Exception as e:
            await self.session.rollback()
            raise HTTPException(status_code=409, detail=f"Ошибка базы данных: {str(e)}")
