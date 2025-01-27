from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from libs.shared.utils.logger import logger
from services.src_auth.app.core.verify_access_token import verify_access_token
from libs.shared.db.database import get_db_ro


class JWTBearer(HTTPBearer):
    """JWT Token authenticater."""

    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(
        self, request: Request, db: Session = Depends(get_db_ro)
    ):
        credentials: HTTPAuthorizationCredentials = await super(
            JWTBearer, self
        ).__call__(request)
        try:
            is_verified_token = verify_access_token(
                credentials.credentials, db=db
            )
            if is_verified_token:
                return credentials.credentials
            else:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token",
                )
        except Exception as e:
            logger.error(f"Invalid token: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )
