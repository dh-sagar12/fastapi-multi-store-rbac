from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, Table, func
from libs.shared.db.database import Base


# class UserStoreAuthGroup(BaseModel):
#     """Association model for store, auth_group and user."""

#     __tablename__ = "user_store_auth_group"

#     id = Column(BigInteger, primary_key=True, nullable=False, index=True)
#     user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
#     store_id = Column(BigInteger, ForeignKey("stores.id"), nullable=False)
#     auth_group_id = Column(
#         BigInteger, ForeignKey("auth_groups.id"), nullable=False
#     )

# relationships

# user  = relationship("User", back_populates="user_store_auth_groups")
# store = relationship("Store", back_populates="user_store_auth_groups")
# auth_group = relationship("AuthGroup", back_populates="user_store_auth_groups")


user_store_auth_groups = Table(
    "user_store_auth_groups",
    Base.metadata,
    Column("user_id", BigInteger, ForeignKey("users.id"), primary_key=True),
    Column("store_id", BigInteger, ForeignKey("stores.id"), primary_key=True),
    Column(
        "auth_group_id",
        BigInteger,
        ForeignKey("auth_groups.id"),
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
