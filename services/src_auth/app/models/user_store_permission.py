"""
Association model definition for MTPermission and User and Store.
"""

from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, Table, func
from libs.shared.db.database import Base


# class UserStorePermission(BaseModel):
#     """Association model definition for auth group and permissions."""

#     __tablename__ = "user_store_permissions"

#     id = Column(BigInteger, primary_key=True, autoincrement=True, index=True)
#     user_id = Column(BigInteger, ForeignKey("users.id"))
#     store_id = Column(BigInteger, ForeignKey("stores.id"))
#     permission_id = Column(BigInteger, ForeignKey("mt_permissions.id"))


user_store_permissions = Table(
    "user_store_permissions",
    Base.metadata,
    Column("user_id", BigInteger, ForeignKey("users.id"), primary_key=True),
    Column("store_id", BigInteger, ForeignKey("stores.id"), primary_key=True),
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
