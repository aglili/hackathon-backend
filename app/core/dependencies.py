from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from fastapi import Depends,HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession
from app.config.database_config import get_db
from app.models.business_user import BusinessUser
from jose import jwt,JWTError
from app.config.settings import settings
from sqlalchemy import select
from uuid import UUID

security = HTTPBearer()




async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db),
) -> BusinessUser:
    """
    Get the current user from the token.
    
    Args:
        credentials: The HTTP authorization credentials.
        db: The database session.
        
    Returns:
        The authenticated business user.
        
    Raises:
        HTTPException: If the credentials cannot be validated.
    """
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        token = credentials.credentials

        payload = jwt.decode(
            token,
            key=settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )


        print(payload)

        user_id = payload.get("id")
        if user_id is None:
            raise credentials_exception
        
    except (JWTError, AttributeError):
        raise credentials_exception
    
    try:
        # Convert string user_id to UUID if necessary
        if isinstance(user_id, str):
            user_id = UUID(user_id)
            
        result = await db.execute(
            select(BusinessUser).where(BusinessUser.id == user_id)
        )

        user = result.scalars().first()
        if user is None:
            raise credentials_exception
        
        return user
    
    except (ValueError, TypeError):
        # Handle invalid UUID format
        raise credentials_exception