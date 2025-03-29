from app.services.base_service import BaseService
from app.repository.business_user_repository import BusinessUserRepository
from app.repository.user_files_repository import UserFilesRepository
from fastapi import Depends
from app.schemas.user_authentication import BusinessUserSignUpRequest,BusinessUserSignInRequest,BusinessUserCompleteOnboardingRequest,FullFile
from app.core.exceptions import InvalidOperationError
from app.helpers.transformers.business_user_transformers import transform_user_to_dict
from app.core.security import generate_access_token,verify_password
from app.helpers import messages
from app.models.business_user import BusinessUser

class BusinessUserService(BaseService):
    def __init__(self, repository: BusinessUserRepository = Depends(BusinessUserRepository),files_repository :UserFilesRepository = Depends(UserFilesRepository) ) -> None:
        self.repository = repository
        self.files_repository = files_repository
        super().__init__(repository)


    async def business_user_signup(self, payload:BusinessUserSignUpRequest) -> dict:
        try:

            existing_user = await self.repository.get_user_by_email(payload.email)
            if existing_user:
                raise InvalidOperationError("User already exists")
            
            user = await self.repository.create(payload)

            user_data = transform_user_to_dict(user=user)


            token,expiry = generate_access_token(user_data)

            return {
                "user": user_data,
                "token": token,
                "expiry": expiry
            }
        except Exception as e:
            raise e
        

    
    async def business_user_signin(self, payload:BusinessUserSignInRequest) -> dict:
        try:
            user = await self.repository.get_user_by_email(payload.email)
            if not user and not verify_password(payload.password, user.password):
                raise InvalidOperationError(messages.INVALID_CREDENTIALS)
            

            user_data = transform_user_to_dict(user=user)

            token,expiry = generate_access_token(user_data)

            return {
                "user": user_data,
                "token": token,
                "expiry": expiry
            }
        except Exception as e:
            raise e
        

    async def complete_onboarding_user(self,user: BusinessUser,payload: BusinessUserCompleteOnboardingRequest) -> dict:
        try:
            user = await self.repository.update(user.id,payload)

            files = payload.files
            if files:
                for file in files:
                    await self.files_repository.create(
                        FullFile(
                            user_id=user.id,
                            file_name=file.file_name,
                            file_url=file.file_url
                        )
                    )

            user_data = transform_user_to_dict(user=user)

            return user_data
        except Exception as e:
            raise e
            








