from datetime import datetime, timedelta
import jwt
import pytz
from libs.shared.config.settings import settings
from services.src_auth.app.core.get_jti import get_jti
from services.src_auth.app.models.refresh_token import RefreshToken
from services.src_auth.app.models.user import User
from sqlalchemy.orm import Session


def encode_access_token(
    user: User, auth_group_id: int, store_id: int, jti: str
):
    """Encode access token."""
    payload = {
        "exp": datetime.now(pytz.UTC)
        + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRES_AT),
        "iat": datetime.now(pytz.UTC),
        "scope": "access_token",
        "jti": jti,
        "user_id": user.id,
        "sub": user.username,
        "store_id": store_id,
        "auth_group_id": auth_group_id,
    }
    return jwt.encode(payload, settings.JWT_SECRET, settings.JWT_ALGORITHM)


def encode_refresh_token(
    user: User,
    auth_group_id: int,
    store_id: int,
    access_token_jti: str,
    db: Session,
):
    payload = {
        "exp": datetime.now(pytz.UTC)
        + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRES_AT),
        "iat": datetime.now(pytz.UTC),
        "scope": "refresh_token",
        "jti": get_jti(),
        "user_id": user.id,
        "sub": user.username,
        "store_id": store_id,
        "auth_group_id": auth_group_id,
    }

    token = jwt.encode(payload, settings.JWT_SECRET, settings.JWT_ALGORITHM)

    # Store refresh token to the database for future use
    db_obj = RefreshToken(
        token=token,
        user_id=user.id,
        access_token_jti=access_token_jti,
    )
    db.add(db_obj)
    db.commit()
    return token
