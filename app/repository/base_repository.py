from fastapi import Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.config.database_config import get_db
from app.core.exceptions import NotFoundError


class BaseRepository:
    def __init__(self, model: None, db: AsyncSession = Depends(get_db)) -> None:
        self.model = model
        self.db = db

    async def create(self, schema):
        query = self.model(**schema.dict())
        try:
            self.db.add(query)
            await self.db.commit()
            await self.db.refresh(query)
            return query
        except IntegrityError as e:
            await self.db.rollback()
            raise e
        except Exception as e:
            await self.db.rollback()
            raise e

    async def read_all(
        self, eager=False, order_by=None, limit: int = 10, page: int = 1, **filters
    ):
        stmt = select(self.model)
        
        if eager:
            for eager_load in getattr(self.model, "eagers", []):
                stmt = stmt.options(selectinload(getattr(self.model, eager_load)))

        for key, value in filters.items():
            stmt = stmt.where(getattr(self.model, key) == value)

        if order_by is not None:
            stmt = stmt.order_by(order_by)

        stmt = stmt.limit(limit).offset((page - 1) * limit)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def read_one(self, id: str, eager=False):
        stmt = select(self.model).where(self.model.id == id)
        
        if eager:
            for eager_load in getattr(self.model, "eagers", []):
                stmt = stmt.options(selectinload(getattr(self.model, eager_load)))
                
        result = await self.db.execute(stmt)
        query = result.scalars().first()
        
        if not query:
            raise NotFoundError(f"{self.model.__name__} with id {id} not found")
        return query

    async def update(self, id: str, schema):
        query = await self.read_one(id)
        for key, value in schema.dict().items():
            setattr(query, key, value)
        await self.db.commit()
        await self.db.refresh(query)
        return query

    async def read_where(self, **filters):
        stmt = select(self.model)
        for key, value in filters.items():
            stmt = stmt.where(getattr(self.model, key) == value)
        result = await self.db.execute(stmt)
        return result.scalars().all()