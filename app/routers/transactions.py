from fastapi import APIRouter, Depends
from app.models.business_user import BusinessUser
from app.core.dependencies import get_current_user
from app.services.transactions_service import TransactionsService
from app.schemas.transactions_schema import CreateTransactionRequestPartial


from app.routers.responses import send_data_with_info, client_side_error, internal_server_error
from app.helpers import messages
from fastapi.responses import ORJSONResponse
from app.core.exceptions import InvalidOperationError


router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"],
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