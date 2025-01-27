from fastapi import status
import jwt
from libs.shared.config.settings import settings
from libs.shared.utils.custom_exception import ServiceException
from libs.shared.utils.logger import logger


def decode_access_token(token: str):
    """Decode access token."""

    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET, [settings.JWT_ALGORITHM]
        )

        if payload["scope"] == "access_token":
            return payload

        raise ServiceException(
            message="Invalid Scope",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    except jwt.ExpiredSignatureError:
        raise ServiceException(
            message="Token Expired",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    except jwt.InvalidTokenError as e:
        logger.error(f"Invalid token: {str(e)}")
        raise ServiceException(
            message="Invalid Token",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )


def decode_refresh_token(token: str):
    """Decode refresh token."""

    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET, [settings.JWT_ALGORITHM]
        )

        if payload["scope"] == "refresh_token":
            return payload

        raise ServiceException(
            message="Invalid Scope",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    except jwt.ExpiredSignatureError:
        raise ServiceException(
            message="Token Expired",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    except jwt.InvalidTokenError as e:
        logger.error(f"Invalid token: {str(e)}")
        raise ServiceException(
            message="Invalid Token",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
