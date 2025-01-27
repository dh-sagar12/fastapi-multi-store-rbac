from fastapi import Depends, HTTPException, status
from libs.shared.auth.get_token_data import get_payload_data
from libs.shared.db.database import get_db
from sqlalchemy.orm import Session

from libs.shared.utils.logger import logger
from services.src_auth.app.models.user import User


def get_current_user(
    payload: str = Depends(get_payload_data),
    db: Session = Depends(get_db),
) -> User:
    try:
        user = db.query(User).filter(User.id == payload.user_id).first()
        return user
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user",
        )
