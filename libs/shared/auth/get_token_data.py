from typing import Optional
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials
from libs.shared.auth.jwt_validator import JWTBearer
from services.src_auth.app.core.decode_tokens import decode_access_token
from services.src_auth.app.schemas.jwt_payload import JWTPayload


def get_payload_data(
    token: Optional[HTTPAuthorizationCredentials] = Depends(JWTBearer()),
) -> JWTPayload:
    payload_data = decode_access_token(token)
    return JWTPayload(**payload_data)
