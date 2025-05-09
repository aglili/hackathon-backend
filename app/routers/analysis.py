from fastapi import APIRouter, Depends
from fastapi.responses import ORJSONResponse
from app.models.business_user import BusinessUser
from app.core.dependencies import get_current_user
from app.services.ai_service import AIService
from app.routers.responses import send_data_with_info, client_side_error, internal_server_error
from app.helpers.enums import ReportType

router = APIRouter(
    prefix="/ai_service",
    tags=["AI Service"],
)



@router.post('/generate_report')
async def generate_report(
    report_type: ReportType,
    user: BusinessUser = Depends(get_current_user),
    ai_service: AIService = Depends(AIService),  
):
    data = user.user_files[0].file_url
    try:
        # Generate report based on historical financial data and report type
        report = await ai_service.create_report(data, report_type,user)

        # get id, report

        return send_data_with_info(
            data=report,
            status_code=200,
            info=f"AI Service generated {report_type} report successfully"
        )
    except Exception as e:
        return internal_server_error(
            user_msg=f"Failed to generate {report_type} report",
            error=str(e),
        )

@router.post('/generate_expenses', response_class=ORJSONResponse)
async def generate_expenses(
    user: BusinessUser = Depends(get_current_user),
    ai_service: AIService = Depends(AIService)
    ):
    try:
        # Generate expenses for the current month
        data_file = user.user_files[0].file_url
        response = await ai_service.generate_expense_data(data_file) 

        summary = await ai_service.generate_expense_summary(response)

        return send_data_with_info(
            data={
                "expenses": response,
                "summary": summary
            },
            status_code=200,
            info="AI Service generated expense data successfully"
        )
    except Exception as e:
        return internal_server_error(
            user_msg="Failed to generate expense data",
            error=str(e),
        )

@router.post('/forecast')
async def forecast_revenue(
    user: BusinessUser = Depends(get_current_user),
    ai_service: AIService = Depends(AIService),
    periods: int = 6
):
    try:
        # Load historical financial data
        data = user.user_files[0].file_url

        # Forecast future revenue
        forecast_data = await ai_service.forecast_revenue(data, periods)

        return send_data_with_info(
            data=forecast_data,
            status_code=200,
            info="AI Service forecasted revenue successfully"
        )
    except Exception as e:
        return internal_server_error(
            user_msg="Failed to forecast revenue",
            error=str(e),
        )
    
@router.post('/generate_smart_index')
async def generate_smart_index(
    user: BusinessUser = Depends(get_current_user),
    ai_service: AIService = Depends(AIService),
):
   data = user.user_files[0].file_url
   try:
       # Generate smart index based on historical financial data
       smart_index = await ai_service.generate_smart_profile(data)

       return send_data_with_info(
           data=smart_index,
           status_code=200,
           info="AI Service generated smart index successfully"
       )
   except Exception as e:
       return internal_server_error(
           user_msg="Failed to generate smart index",
           error=str(e),
       )
   
@router.post('/recommendations')
async def generate_recommendations(
    user: BusinessUser = Depends(get_current_user),
    ai_service: AIService = Depends(AIService),
):
    data = user.user_files[0].file_url
    try:
        # Generate recommendations based on historical financial data
        recommendations = await ai_service.generate_score_improvement_recommendations(data)

        return send_data_with_info(
            data=recommendations,
            status_code=200,
            info="AI Service generated recommendations successfully"
        )
    except Exception as e:
        return internal_server_error(
            user_msg="Failed to generate recommendations",
            error=str(e),
        )
    
@router.post('/generate_report')
async def generate_report(
    report_type: ReportType,
    user: BusinessUser = Depends(get_current_user),
    ai_service: AIService = Depends(AIService),  
):
    data = user.user_files[0].file_url
    try:
        # Generate report based on historical financial data and report type
        report = await ai_service.create_report(data, report_type,user)

        # get id, report

        return send_data_with_info(
            data=report,
            status_code=200,
            info=f"AI Service generated {report_type} report successfully"
        )
    except Exception as e:
        return internal_server_error(
            user_msg=f"Failed to generate {report_type} report",
            error=str(e),
        )
    
@router.post('/financial_info')
async def get_financial_info(
    user: BusinessUser = Depends(get_current_user),
    ai_service: AIService = Depends(AIService),
):
    try:
        data = user.user_files[0].file_url
        # Get financial info based on historical financial data
        financial_info = await ai_service.generate_financial_info(data)

        return send_data_with_info(
            data=financial_info,
            status_code=200,
            info="AI Service fetched financial info successfully"
        )
    except Exception as e:
        return internal_server_error(
            user_msg="Failed to fetch financial info",
            error=str(e),
        )
