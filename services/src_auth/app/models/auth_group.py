"""
Database model definition for auth group.
"""

from sqlalchemy import Column, BigInteger, String
from sqlalchemy.orm import relationship

from libs.shared.utils.base_model import BaseModel
from services.src_auth.app.models.auth_group_permission import (
    auth_group_permissions,
)
from services.src_auth.app.models.user_store_auth_group import (
    user_store_auth_groups,
)


class AuthGroup(BaseModel):
    """Auth group model."""

    __tablename__ = "auth_groups"

    id = Column(BigInteger, primary_key=True, nullable=False, index=True)
    name = Column(String(50), nullable=False, unique=True, index=True)

    # many-tomany relationships
    permissions = relationship(
        "Permission",
        secondary=auth_group_permissions,
        back_populates="auth_groups",
    )
    users = relationship(
        "User",
        secondary=user_store_auth_groups,
        back_populates="auth_groups",
        overlaps="stores,auth_groups",
    )
    stores = relationship(
        "Store",
        secondary=user_store_auth_groups,
        back_populates="auth_groups",
        overlaps="users,auth_groups",
    )
