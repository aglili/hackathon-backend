from pydantic import BaseModel,field_validator,EmailStr
import re
from app.config.settings import settings
from app.core.exceptions import InvalidOperationError
from app.helpers import messages
from app.core.security import hash_password
from app.helpers.enums import BusinessType, BusinessIndustry
import datetime



class BusinessUserSignUpRequest(BaseModel):
    email: EmailStr
    password: str
    

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, value: str) -> str:
        # Validate password strength with regex
        if not re.match(settings.PASSWORD_REGEX, value):
            raise InvalidOperationError(messages.PASSWORD_REQUIREMENT)
        return hash_password(value)


class BusinessUserSignInRequest(BaseModel):
    email: EmailStr
    password: str



class BusinessUserCompleteOnboardingRequest(BaseModel):
    business_name: str
    business_type: BusinessType
    industry: BusinessIndustry
    registration_date: datetime.date
    location: str
    no_of_employees: int

    # @field_validator("registration_date")
    # @classmethod
    # def validate_registration_date(cls, value: str) -> str:
    #     # Validate date format (YYYY-MM-DD)
    #     if not re.match(r"^\d{4}-\d{2}-\d{2}$", value):
    #         raise InvalidOperationError(messages.INVALID_DATE_FORMAT)
    #     return value
    

    # @field_validator("registration_date")
    # @classmethod
    # def validate_registration_date(cls, value: str) -> str:
    #     # make sure date is not in the future
    #     if value > str(datetime.date.today()):
    #         raise InvalidOperationError(messages.DATE_IN_FUTURE)
    #     return value
    
    @field_validator("no_of_employees")
    @classmethod
    def validate_no_of_employees(cls, value: int) -> int:
        # Validate that no_of_employees is a positive integer
        if value <= 0:
            raise InvalidOperationError(messages.INVALID_NO_OF_EMPLOYEES)
        return value

   