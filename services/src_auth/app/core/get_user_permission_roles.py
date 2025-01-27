from sqlalchemy import and_, select, union
from services.src_auth.app.models.user_store_permission import (
    user_store_permissions,
)
from services.src_auth.app.models.auth_group_permission import (
    auth_group_permissions,
)
from services.src_auth.app.models.permission import Permission


def get_role_and_user_permissions(*, user_id, role_id, store_id, db):
    auth_group_query = (
        select(Permission.code)
        .select_from(auth_group_permissions)
        .join(
            Permission, auth_group_permissions.c.permission_id == Permission.id
        )
        .where(auth_group_permissions.c.auth_group_id == role_id)
    )

    # Query for user store permissions
    user_store_query = (
        select(Permission.code)
        .select_from(user_store_permissions)
        .join(
            Permission, user_store_permissions.c.permission_id == Permission.id
        )
        .where(
            and_(
                user_store_permissions.c.user_id == user_id,
                user_store_permissions.c.store_id == store_id,
            )
        )
    )

    combined_query = union(auth_group_query, user_store_query)
    result = db.execute(combined_query)
    return [row[0] for row in result]
