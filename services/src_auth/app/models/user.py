from sqlalchemy import (
    BigInteger,
    Column,
    DateTime,
    ForeignKey,
    String,
    Text,
)
from libs.shared.utils.base_model import BaseModel
from sqlalchemy.orm import relationship
from services.src_auth.app.models.user_store_auth_group import (
    user_store_auth_groups,
)
from services.src_auth.app.models.user_store_permission import (
    user_store_permissions,
)


class User(BaseModel):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, autoincrement=True, index=True)
    username = Column(String(255), nullable=False, unique=True, index=True)
    password = Column(Text, nullable=False)
    first_name = Column(String(255))
    last_name = Column(String(255))
    first_name_kana = Column(String(255), index=True)
    last_name_kana = Column(String(255), index=True)
    primary_store_id = Column(
        BigInteger, ForeignKey("stores.id"), nullable=False
    )
    last_logged_in = Column(DateTime)

    primary_store = relationship("Store", back_populates="users")
    refresh_tokens = relationship("RefreshToken", back_populates="user")
    token_blacklists = relationship("TokenBlacklist", back_populates="user")

    # Many-to-Many Relationships
    stores = relationship(
        "Store",
        secondary=user_store_auth_groups,
        back_populates="users",
        overlaps="auth_groups,stores",
    )
    auth_groups = relationship(
        "AuthGroup",
        secondary=user_store_auth_groups,
        back_populates="users",
        overlaps="stores,auth_groups",
    )
    permissions = relationship(
        "Permission",
        secondary=user_store_permissions,
        back_populates="users",
        overlaps="stores,permissions",
    )
