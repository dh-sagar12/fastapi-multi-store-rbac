from sqlalchemy import BigInteger, Column, ForeignKey, String, UniqueConstraint
from libs.shared.utils.base_model import BaseModel
from sqlalchemy.orm import relationship

from services.src_auth.app.models.user_store_auth_group import (
    user_store_auth_groups,
)
from services.src_auth.app.models.user_store_permission import (
    user_store_permissions,
)


class Store(BaseModel):
    __tablename__ = "stores"

    id = Column(BigInteger, primary_key=True, autoincrement=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    full_name = Column(String(255), nullable=True, index=True)
    postal_code = Column(String(30), nullable=True)
    phone_number = Column(String(20), nullable=True)
    city_id = Column(BigInteger, ForeignKey("cities.id"), nullable=True)
    prefecture = Column(String(100), nullable=True)
    street = Column(String(100), nullable=True)
    building_name = Column(String(100), nullable=True)

    city = relationship("City", back_populates="stores")

    # Adding Indexes
    __table_args__ = (UniqueConstraint("name", name="uix_stores_name"),)

    users = relationship("User", back_populates="primary_store")

    users = relationship(
        "User",
        secondary=user_store_auth_groups,
        back_populates="stores",
        overlaps="auth_groups,users",
    )
    auth_groups = relationship(
        "AuthGroup",
        secondary=user_store_auth_groups,
        back_populates="stores",
        overlaps="users,auth_groups",
    )
    permissions = relationship(
        "Permission",
        secondary=user_store_permissions,
        back_populates="stores",
        overlaps="users,permissions",
    )
