from sqlalchemy import BigInteger, Column, String
from libs.shared.utils.base_model import BaseModel
from sqlalchemy.orm import relationship

from services.src_auth.app.models.auth_group_permission import (
    auth_group_permissions,
)
from services.src_auth.app.models.user_store_permission import (
    user_store_permissions,
)


class Permission(BaseModel):
    __tablename__ = "mt_permissions"

    id = Column(BigInteger, primary_key=True, autoincrement=True, index=True)
    name = Column(String(255), nullable=False)
    code = Column(String(255), nullable=False, unique=True, index=True)

    auth_groups = relationship(
        "AuthGroup",
        secondary=auth_group_permissions,
        back_populates="permissions",
    )
    users = relationship(
        "User",
        secondary=user_store_permissions,
        back_populates="permissions",
        overlaps="stores,permissions",
    )
    stores = relationship(
        "Store",
        secondary=user_store_permissions,
        back_populates="permissions",
        overlaps="users,permissions",
    )
