from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.core.settings import settings

http_bearer = HTTPBearer()

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


async def check_internal_service_token(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(http_bearer)],
) -> bool:
    internal_service_token = credentials.credentials
    if internal_service_token in (settings.INTERNAL_SERVICE_TOKEN,):
        return True
    else:
        return False
