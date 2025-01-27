from dataclasses import dataclass
import datetime


@dataclass
class JWTPayload:
    exp: datetime
    iat: datetime
    scope: str
    jti: str
    user_id: int
    sub: str
    store_id: int
    auth_group_id: int
