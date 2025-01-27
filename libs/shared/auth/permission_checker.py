from functools import lru_cache
from fastapi import Depends, HTTPException, status

from libs.shared.auth.get_current_user import get_current_user
from libs.shared.auth.get_token_data import get_payload_data
from libs.shared.db.database import get_db_ro
from services.src_auth.app.core.get_user_permission_roles import (
    get_role_and_user_permissions,
)
from services.src_auth.app.models.user import User
from services.src_auth.app.schemas.jwt_payload import JWTPayload


def has_permission(required_permissions: list[str]):

    required_perm_set = frozenset(required_permissions)

    @lru_cache(maxsize=1024)
    def cache_permissions(
        user_id: int, role_id: int, store_id: int
    ) -> frozenset:
        """Cache permission results for each unique combination of parameters"""
        return frozenset(
            get_role_and_user_permissions(
                user_id=user_id,
                role_id=role_id,
                store_id=store_id,
                db=next(get_db_ro()),
            )
        )

    async def dependency(
        user: User = Depends(get_current_user),
        payload: JWTPayload = Depends(get_payload_data),
    ):

        if payload.auth_group_id == 1:
            return True

        available_permissions = cache_permissions(
            user_id=user.id,
            role_id=payload.auth_group_id,
            store_id=payload.store_id,
        )

        if not required_perm_set.issubset(available_permissions):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )

        return True

    return Depends(dependency)
