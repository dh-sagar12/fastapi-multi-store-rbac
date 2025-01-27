from sqlalchemy.orm import Session

from services.src_auth.app.models.token_blacklist import TokenBlacklist


def is_access_token_blacklisted(token: str, db: Session) -> bool:
    """Check if token is revoked."""

    token = (
        db.query(TokenBlacklist).filter(TokenBlacklist.token == token).first()
    )
    if token:
        return True

    return False
