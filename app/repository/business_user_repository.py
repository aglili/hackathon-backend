from app.repository.base_repository import BaseRepository
from app.models.business_user import BusinessUser
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.config.database_config import get_db
from typing import Optional
from sqlalchemy import select



class BusinessUserRepository(BaseRepository):
    def __init__(self, db: AsyncSession = Depends(get_db)) -> None:
        super().__init__(BusinessUser, db)


    async def get_user_by_email(self, email: str) -> Optional[BusinessUser]:
        """
        Get a user by email.
        """
        stmt = select(self.model).where(self.model.email == email)
        result = await self.db.execute(stmt)
        return result.scalars().first()
    

