from app.repository.base_repository import BaseRepository
from app.models.business_user import UserFiles
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.config.database_config import get_db





class UserFilesRepository(BaseRepository):
    def __init__(self, db: AsyncSession = Depends(get_db)) -> None:
        super().__init__(UserFiles, db)
