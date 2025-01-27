from services.src_auth.app.core.decode_tokens import decode_access_token
from sqlalchemy.orm import Session

from services.src_auth.app.core.is_access_token_blacklisted import (
    is_access_token_blacklisted,
)


def verify_access_token(token: str, db: Session) -> bool:
    is_token_blacklisted = is_access_token_blacklisted(token, db)
    if is_token_blacklisted:
        raise False
    payload = decode_access_token(token)
    if not payload:
        raise False

    return True
