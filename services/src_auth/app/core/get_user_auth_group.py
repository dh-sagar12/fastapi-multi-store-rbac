from sqlalchemy import and_, select
from sqlalchemy.orm import Session
from services.src_auth.app.models.user_store_auth_group import (
    user_store_auth_groups,
)


def get_user_auth_group(*, user_id: int, store_id: int, db: Session):

    query = select(user_store_auth_groups).where(
        and_(
            user_store_auth_groups.c.user_id == user_id,
            user_store_auth_groups.c.store_id == store_id,
        )
    )

    result = db.execute(query)
    return result.mappings().first()
