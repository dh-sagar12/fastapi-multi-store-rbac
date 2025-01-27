"""
Association model definition for MTPermission and AuthGroup.
"""

from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, Table, func
from libs.shared.db.database import Base


# class AuthGroupPermission(BaseModel):
#     """Association model definition for auth group and permissions."""

#     __tablename__ = "auth_group_permissions"

#     id = Column(BigInteger, primary_key=True, autoincrement=True, index=True)
#     group_id = Column(BigInteger, ForeignKey("auth_groups.id"), nullable=False)
#     permission_id = Column(
#         BigInteger, ForeignKey("mt_permissions.id"), nullable=False
#     )


auth_group_permissions = Table(
    "auth_group_permissions",
    Base.metadata,
    Column(
        "auth_group_id",
        BigInteger,
        ForeignKey("auth_groups.id"),
        primary_key=True,
    ),
    Column(
        "permission_id",
        BigInteger,
        ForeignKey("mt_permissions.id"),
        primary_key=True,
    ),
    Column(
        "created_at",
        DateTime(timezone=True),
        default=func.now(),
        nullable=False,
        index=True,
    ),
    Column(
        "updated_at",
        DateTime(timezone=True),
        default=func.now(),
        onupdate=func.now(),
        nullable=False,
        index=True,
    ),
    Column(
        "deleted_at",
        DateTime(timezone=True),
        default=None,
        nullable=True,
        index=True,
    ),
)
