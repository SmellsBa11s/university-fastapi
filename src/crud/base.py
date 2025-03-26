from fastapi import Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import insert, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.core.db.database import get_async_db


class BaseDAO:
    """Abstract Data Access Object (DAO) with basic CRUD operations.

    Requires setting the `model` attribute in child classes.
    Automatically manages sessions through dependency injection.

    Attributes:
        model (DeclarativeBase): SQLAlchemy model for operations
    """

    model = None

    def __init__(self, session: AsyncSession = Depends(get_async_db)):
        """Initializes DAO with a database session.

        Args:
            session (AsyncSession): Asynchronous SQLAlchemy session,
                injected through FastAPI Depends
        """
        self.session = session

    async def add(self, data: dict | BaseModel):
        """Creates a new record in the database.

        Args:
            data (dict | BaseModel): Dictionary or Pydantic model
                with data for creation

        Returns:
            model: Created model instance

        Raises:
            ValueError: For empty or invalid data
            SQLAlchemyError: For database operation errors
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
            raise HTTPException(status_code=409, detail=f"Database error: {str(e)}")

    async def find_one(self, **filter_by):
        """Finds one record by given filters.

        Args:
            **filter_by: Arguments for WHERE condition
                (example: username="john")

        Returns:
            model: Found model object
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
        """Finds one record by given filters.

        Args:
            **filter_by: Arguments for WHERE condition
                (example: username="john")

        Returns:
            model: Found model object or None if not found (for special cases)
        """
        query = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(query)
        return res.scalar_one_or_none()

    async def find_all(self, **filter_by):
        """Finds all records by given filters.

        Args:
            **filter_by: Arguments for WHERE condition
                (example: is_active=True)

        Returns:
            list[model]: List of found model objects
        """
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def delete(self, model_id: int):
        """Deletes a record by ID.

        Args:
            model_id (int): Record ID to delete

        Returns:
            bool | None: True if deletion was successful,
                None if record was not found
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
        """Updates a record by ID.

        Args:
            model_id (int): Record ID to update
            **update_data: Data to update
                (example: username="new_name")

        Returns:
            model | None: Updated model object
                or None if record was not found
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
            raise HTTPException(status_code=409, detail=f"Database error: {str(e)}")
