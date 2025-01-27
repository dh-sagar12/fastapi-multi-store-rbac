from typing import List

from sqlalchemy import and_, func, insert, update
from libs.shared.utils.base_crud import CRUDBase
from services.src_auth.app.models import Permission
from services.src_auth.app.models.user_store_permission import (
    user_store_permissions,
)
from services.src_auth.app.models.auth_group_permission import (
    auth_group_permissions,
)
from services.src_auth.app.schemas.permission import CreatePermission


class PermissionService(
    CRUDBase[Permission, CreatePermission, CreatePermission]
):

    def assign_permission_to_auth_group(
        self,
        auth_group_id: int,
        permission_ids: List[int],
    ):

        with self.db.begin() as transaction:
            # Step 1: Soft-delete existing permissions not in the new list
            update_stmt = (
                update(auth_group_permissions)
                .where(
                    and_(
                        auth_group_permissions.c.auth_group_id
                        == auth_group_id,
                        auth_group_permissions.c.permission_id.notin_(
                            permission_ids
                        ),
                        auth_group_permissions.c.deleted_at.is_(None),
                    )
                )
                .values(deleted_at=func.now(), updated_at=func.now())
            )
            self.db.execute(update_stmt)

            # Step 2: Insert or reactivate permissions in the list
            if permission_ids:
                values = [
                    {
                        "auth_group_id": auth_group_id,
                        "permission_id": pid,
                        "created_at": func.now(),
                        "updated_at": func.now(),
                        "deleted_at": None,
                    }
                    for pid in permission_ids
                ]

                stmt = insert(auth_group_permissions).values(values)
                stmt = stmt.on_conflict_do_update(
                    index_elements=["auth_group_id", "permission_id"],
                    set_={
                        "deleted_at": None,
                        "updated_at": func.now(),
                    },
                    where=(auth_group_permissions.c.deleted_at.isnot(None)),
                )

                self.db.execute(stmt)

            transaction.commit()

        return {"message": "Permissions assigned successfully"}

    def assign_permission_to_users(
        self,
        *,
        user_id: int,
        store_id: int,
        permission_ids: List[int],
    ):

        with self.db.begin() as transaction:
            # Step 1: Soft-delete existing permissions not in the new list
            update_stmt = (
                update(user_store_permissions)
                .where(
                    and_(
                        user_store_permissions.c.user_id == user_id,
                        user_store_permissions.c.store_id == store_id,
                        user_store_permissions.c.permission_id.notin_(
                            permission_ids
                        ),
                        user_store_permissions.c.deleted_at.is_(None),
                    )
                )
                .values(deleted_at=func.now(), updated_at=func.now())
            )
            self.db.execute(update_stmt)

            # Step 2: Insert or reactivate permissions in the list
            if permission_ids:
                values = [
                    {
                        "user_id": user_id,
                        "store_id": store_id,
                        "permission_id": pid,
                        "created_at": func.now(),
                        "updated_at": func.now(),
                        "deleted_at": None,
                    }
                    for pid in permission_ids
                ]

                stmt = insert(user_store_permissions).values(values)
                stmt = stmt.on_conflict_do_update(
                    index_elements=["user_id", "store_id", "permission_id"],
                    set_={
                        "deleted_at": None,
                        "updated_at": func.now(),
                    },
                    where=(user_store_permissions.c.deleted_at.isnot(None)),
                )

                self.db.execute(stmt)

            transaction.commit()

        return {"message": "Permissions assigned successfully"}
