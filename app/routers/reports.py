from fastapi import Depends, APIRouter
from app.services.reports_service import ReportsService
from app.models.business_user import BusinessUser
from app.core.dependencies import get_current_user
from app.routers.responses import send_data_with_info,client_side_error,internal_server_error
from app.core.exceptions import NotFoundError



router = APIRouter(
    prefix="/reports",
    tags=["Reports"],
)


@router.get("/", response_model=dict)
async def get_reports(
    user: BusinessUser = Depends(get_current_user),
    page: int = 1,
    limit: int = 10,
    reports_service: ReportsService = Depends(ReportsService),
) -> dict:
    try:
        response = await reports_service.get_reports(user=user, page=page, limit=limit)
        return send_data_with_info(
            data=response,
            status_code=200,
            info="Reports fetched successfully",
        )
    except NotFoundError as e:
        return client_side_error(
            user_msg=str(e.detail),
            status_code=404,
        )
    except Exception as e:
        return internal_server_error(
            user_msg="Failed to fetch reports",
            error=str(e),
        )
    


@router.get("/{report_id}", response_model=dict)
async def get_report_by_id(
    report_id: str,
    user: BusinessUser = Depends(get_current_user),
    reports_service: ReportsService = Depends(ReportsService),
) -> dict:
    try:
        response = await reports_service.get_report_by_id(user=user, report_id=report_id)
        return send_data_with_info(
            data=response,
            status_code=200,
            info="Report fetched successfully",
        )
    except NotFoundError as e:
        return client_side_error(
            user_msg=str(e.detail),
            status_code=404,
        )
    except Exception as e:
        return internal_server_error(
            user_msg="Failed to fetch report",
            error=str(e),
        )