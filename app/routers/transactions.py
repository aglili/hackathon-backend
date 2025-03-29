from fastapi import APIRouter, Depends
from app.models.business_user import BusinessUser
from app.core.dependencies import get_current_user
from app.services.transactions_service import TransactionsService
from app.schemas.transactions_schema import CreateTransactionRequestPartial
from app.helpers.enums import TransactionCategory, TransactionType
from datetime import date


from app.routers.responses import send_data_with_info, client_side_error, internal_server_error
from app.helpers import messages
from fastapi.responses import ORJSONResponse
from app.core.exceptions import InvalidOperationError


router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"],
)

dashboard_router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)

@router.post("/", response_class=ORJSONResponse)
async def create_transaction(
    payload: CreateTransactionRequestPartial,
    user: BusinessUser = Depends(get_current_user),
    transaction_service: TransactionsService = Depends(TransactionsService),
) -> dict:
    try:
        response = await transaction_service.create_transaction(user, payload)
        return send_data_with_info(
            data=response,
            status_code=201,
            info=messages.CREATE_SUCCESS + "transaction",
        )
    except InvalidOperationError as e:
        return client_side_error(
            user_msg=str(e.detail),
            status_code=400,
        )
    except Exception as e:
        return internal_server_error(
            user_msg=messages.CREATE_FAILED + "transaction",
            error=str(e),
        )
    

@router.get("/", response_class=ORJSONResponse)
async def get_transactions(
    user: BusinessUser = Depends(get_current_user),
    page: int = 1,
    limit: int = 10,
    transaction_service: TransactionsService = Depends(TransactionsService),
    category: TransactionCategory = None,
    type: TransactionType = None,
    search_string: str = None,
    start_date: date = None,
    end_date: date = None,
) -> dict:
    try:
        response = await transaction_service.get_transactions(user, page, limit,category, type, search_string, start_date, end_date)
        return send_data_with_info(
            data=response,
            status_code=200,
            info=messages.GET_SUCCESS + "transactions",
        )
    except InvalidOperationError as e:
        return client_side_error(
            user_msg=str(e.detail),
            status_code=400,
        )
    except Exception as e:
        return internal_server_error(
            user_msg=messages.GET_FAILED + "transactions",
            error=str(e),
        )
    

@dashboard_router.get("/overview", response_class=ORJSONResponse)
async def get_overview(
    user: BusinessUser = Depends(get_current_user),
    transaction_service: TransactionsService = Depends(TransactionsService),
) -> dict:
    try:
        response = await transaction_service.get_overview(user)
        return send_data_with_info(
            data=response,
            status_code=200,
            info=messages.GET_SUCCESS + "dashboard overview",
        )
    except Exception as e:
        return internal_server_error(
            user_msg=messages.GET_FAILED + "dashboard overview",
            error=str(e),
        )


@dashboard_router.get("/income-expense", response_class=ORJSONResponse)
async def get_income_expense(
    user: BusinessUser = Depends(get_current_user),
    transaction_service: TransactionsService = Depends(TransactionsService),
) -> dict:
    try:
        response = await transaction_service.get_monthly_income_and_expenses(user)
        return send_data_with_info(
            data=response,
            status_code=200,
            info=messages.GET_SUCCESS + "dashboard income and expense",
        )
    except Exception as e:
        return internal_server_error(
            user_msg=messages.GET_FAILED + "dashboard income and expense",
            error=str(e),
        )