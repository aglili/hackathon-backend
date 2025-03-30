from app.services.base_service import BaseService
from app.repository.reports_repository import ReportsRepository
from fastapi import Depends
from app.models.business_user import BusinessUser
from app.helpers.utils import generate_pagination_metadata
from app.helpers.transformers.reports_transformer import transform_report_to_dict
from app.core.exceptions import NotFoundError



class ReportsService(BaseService):
    def __init__(self, repository:ReportsRepository = Depends(ReportsRepository)) -> None:
        self.repository = repository
        super().__init__(repository)



    async def get_reports(self, user: BusinessUser,page: int = 1,limit: int = 10) -> dict:
        try:
            reports = await self.repository.get_reports(user_id=user.id,page=page,limit=limit)

            total_reports = await self.repository.get_reports_count(user_id=user.id)


            return {
                "reports": [transform_report_to_dict(report=report) for report in reports],
                "pagination": generate_pagination_metadata(
                    total_records=total_reports,
                    page=page,
                    limit=limit
                )
            }
        except Exception as e:
            raise e
        
    
    async def get_report_by_id(self, user: BusinessUser, report_id: str) -> dict:
        try:
            report = await self.repository.get_report_by_id(report_id=report_id,user_id=user.id)
            if not report:
                raise NotFoundError("Report not found")
            
            return transform_report_to_dict(report=report)
        except Exception as e:
            raise e
        

    
        
            


