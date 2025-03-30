from app.repository.base_repository import BaseRepository
from app.models.reports import Businessreports
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.config.database_config import get_db
from typing import Optional,List
from sqlalchemy import select,func





class ReportsRepository(BaseRepository):
    def __init__(self, db: AsyncSession = Depends(get_db)) -> None:
        super().__init__(Businessreports, db)



    async def get_reports(self, user_id: str, page: int = 1, limit: int = 10) -> List[Businessreports]:
        """
        Get all reports for a user, sorted by creation date.
        """
        stmt = select(self.model).where(self.model.user_id == user_id).order_by(self.model.created_at.desc())
        stmt = stmt.limit(limit).offset((page - 1) * limit)
        result = await self.db.execute(stmt)
        return result.scalars().all()
    
    async def get_reports_count(self, user_id: str) -> int:
        """
        Get the count of reports for a user.
        """
        stmt = select(func.count(self.model.id)).where(self.model.user_id == user_id) # changed the query
        result = await self.db.execute(stmt)
        return result.scalar() 

    

    async def get_report_by_id(self, report_id: str,user_id:str) -> Optional[Businessreports]:
        """
        Get a report by its ID.
        """
        stmt = select(self.model).where(self.model.id == report_id, self.model.user_id == user_id)
        result = await self.db.execute(stmt)
        return result.scalars().first()