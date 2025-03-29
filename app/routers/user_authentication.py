from app.services.business_user_service import BusinessUserService
from fastapi import APIRouter, Depends
from app.routers.responses import send_data_with_info,client_side_error,internal_server_error
from app.core.exceptions import InvalidOperationError
from app.schemas.user_authentication import BusinessUserSignUpRequest,BusinessUserSignInRequest,BusinessUserCompleteOnboardingRequest
from app.helpers import messages
from fastapi.responses import ORJSONResponse
from app.models.business_user import BusinessUser
from app.core.dependencies import get_current_user




router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post("/signup", response_class=ORJSONResponse)
async def signup(
    payload: BusinessUserSignUpRequest,
    user_service: BusinessUserService = Depends(BusinessUserService),
) -> dict:  
    try:
        response = await user_service.business_user_signup(payload)
        return send_data_with_info(
            data=response,
            status_code=201,
            info=messages.CREATE_SUCCESS + "user",
        )
    except InvalidOperationError as e:
        return client_side_error(
            user_msg=str(e.detail),
            status_code=400,
        )
    except Exception as e:
        return internal_server_error(
            user_msg=messages.CREATE_FAILED + "user",
            error=str(e),
        )
    


@router.post("/signin", response_class=ORJSONResponse)
async def signin(
    payload: BusinessUserSignInRequest,
    user_service: BusinessUserService = Depends(BusinessUserService),
) -> dict:
    try:
        response = await user_service.business_user_signin(payload)
        return send_data_with_info(
            data=response,
            status_code=200,
            info=messages.LOGIN_SUCCESS + "user",
        )
    except InvalidOperationError as e:
        return client_side_error(
            user_msg=str(e.detail),
            status_code=400,
        )
    except Exception as e:
        return internal_server_error(
            user_msg=messages.LOGIN_FAILED + "user",
            error=str(e),
        )



@router.patch("/", response_class=ORJSONResponse)
async def complete_onboarding_user(
    payload: BusinessUserCompleteOnboardingRequest,
    user_service: BusinessUserService = Depends(BusinessUserService),
    current_user: BusinessUser = Depends(get_current_user),
) -> dict:
    try:
        response = await user_service.complete_onboarding_user(user=current_user,payload=payload)
        return send_data_with_info(
            data=response,
            status_code=200,
            info=messages.UPDATE_SUCCESS + "user",
        )
    except InvalidOperationError as e:
        return client_side_error(
            user_msg=str(e.detail),
            status_code=400,
        )
    except Exception as e:
        return internal_server_error(
            user_msg=messages.UPDATE_FAILED + "user",
            error=str(e),
        )