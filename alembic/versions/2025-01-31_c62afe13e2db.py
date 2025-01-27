"""revision

Revision ID: c62afe13e2db
Revises:
Create Date: 2025-01-31 05:09:33.363709

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c62afe13e2db"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "auth_groups",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_auth_groups_created_at"),
        "auth_groups",
        ["created_at"],
        unique=False,
    )
    op.create_index(
        op.f("ix_auth_groups_deleted_at"),
        "auth_groups",
        ["deleted_at"],
        unique=False,
    )
    op.create_index(
        op.f("ix_auth_groups_id"), "auth_groups", ["id"], unique=False
    )
    op.create_index(
        op.f("ix_auth_groups_name"), "auth_groups", ["name"], unique=True
    )
    op.create_index(
        op.f("ix_auth_groups_updated_at"),
        "auth_groups",
        ["updated_at"],
        unique=False,
    )
    op.create_table(
        "cities",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("postal_code", sa.String(length=30), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_index(
        op.f("ix_cities_created_at"), "cities", ["created_at"], unique=False
    )
    op.create_index(
        op.f("ix_cities_deleted_at"), "cities", ["deleted_at"], unique=False
    )
    op.create_index(op.f("ix_cities_id"), "cities", ["id"], unique=False)
    op.create_index(
        op.f("ix_cities_updated_at"), "cities", ["updated_at"], unique=False
    )
    op.create_table(
        "mt_permissions",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("code", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_mt_permissions_code"), "mt_permissions", ["code"], unique=True
    )
    op.create_index(
        op.f("ix_mt_permissions_created_at"),
        "mt_permissions",
        ["created_at"],
        unique=False,
    )
    op.create_index(
        op.f("ix_mt_permissions_deleted_at"),
        "mt_permissions",
        ["deleted_at"],
        unique=False,
    )
    op.create_index(
        op.f("ix_mt_permissions_id"), "mt_permissions", ["id"], unique=False
    )
    op.create_index(
        op.f("ix_mt_permissions_updated_at"),
        "mt_permissions",
        ["updated_at"],
        unique=False,
    )
    op.create_table(
        "auth_group_permissions",
        sa.Column("auth_group_id", sa.BigInteger(), nullable=False),
        sa.Column("permission_id", sa.BigInteger(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["auth_group_id"],
            ["auth_groups.id"],
        ),
        sa.ForeignKeyConstraint(
            ["permission_id"],
            ["mt_permissions.id"],
        ),
        sa.PrimaryKeyConstraint("auth_group_id", "permission_id"),
    )
    op.create_index(
        op.f("ix_auth_group_permissions_created_at"),
        "auth_group_permissions",
        ["created_at"],
        unique=False,
    )
    op.create_index(
        op.f("ix_auth_group_permissions_deleted_at"),
        "auth_group_permissions",
        ["deleted_at"],
        unique=False,
    )
    op.create_index(
        op.f("ix_auth_group_permissions_updated_at"),
        "auth_group_permissions",
        ["updated_at"],
        unique=False,
    )
    op.create_table(
        "stores",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("full_name", sa.String(length=255), nullable=True),
        sa.Column("postal_code", sa.String(length=30), nullable=True),
        sa.Column("phone_number", sa.String(length=20), nullable=True),
        sa.Column("city_id", sa.BigInteger(), nullable=True),
        sa.Column("prefecture", sa.String(length=100), nullable=True),
        sa.Column("street", sa.String(length=100), nullable=True),
        sa.Column("building_name", sa.String(length=100), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["city_id"],
            ["cities.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
        sa.UniqueConstraint("name", name="uix_stores_name"),
    )
    op.create_index(
        op.f("ix_stores_created_at"), "stores", ["created_at"], unique=False
    )
    op.create_index(
        op.f("ix_stores_deleted_at"), "stores", ["deleted_at"], unique=False
    )
    op.create_index(
        op.f("ix_stores_full_name"), "stores", ["full_name"], unique=False
    )
    op.create_index(op.f("ix_stores_id"), "stores", ["id"], unique=False)
    op.create_index(
        op.f("ix_stores_updated_at"), "stores", ["updated_at"], unique=False
    )
    op.create_table(
        "users",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("username", sa.String(length=255), nullable=False),
        sa.Column("password", sa.Text(), nullable=False),
        sa.Column("first_name", sa.String(length=255), nullable=True),
        sa.Column("last_name", sa.String(length=255), nullable=True),
        sa.Column("first_name_kana", sa.String(length=255), nullable=True),
        sa.Column("last_name_kana", sa.String(length=255), nullable=True),
        sa.Column("primary_store_id", sa.BigInteger(), nullable=False),
        sa.Column("last_logged_in", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["primary_store_id"],
            ["stores.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_users_created_at"), "users", ["created_at"], unique=False
    )
    op.create_index(
        op.f("ix_users_deleted_at"), "users", ["deleted_at"], unique=False
    )
    op.create_index(
        op.f("ix_users_first_name_kana"),
        "users",
        ["first_name_kana"],
        unique=False,
    )
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)
    op.create_index(
        op.f("ix_users_last_name_kana"),
        "users",
        ["last_name_kana"],
        unique=False,
    )
    op.create_index(
        op.f("ix_users_updated_at"), "users", ["updated_at"], unique=False
    )
    op.create_index(
        op.f("ix_users_username"), "users", ["username"], unique=True
    )
    op.create_table(
        "refresh_tokens",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("token", sa.Text(), nullable=False),
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("access_token_jti", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_refresh_tokens_access_token_jti"),
        "refresh_tokens",
        ["access_token_jti"],
        unique=True,
    )
    op.create_index(
        op.f("ix_refresh_tokens_created_at"),
        "refresh_tokens",
        ["created_at"],
        unique=False,
    )
    op.create_index(
        op.f("ix_refresh_tokens_deleted_at"),
        "refresh_tokens",
        ["deleted_at"],
        unique=False,
    )
    op.create_index(
        op.f("ix_refresh_tokens_id"), "refresh_tokens", ["id"], unique=False
    )
    op.create_index(
        op.f("ix_refresh_tokens_token"),
        "refresh_tokens",
        ["token"],
        unique=True,
    )
    op.create_index(
        op.f("ix_refresh_tokens_updated_at"),
        "refresh_tokens",
        ["updated_at"],
        unique=False,
    )
    op.create_index(
        op.f("ix_refresh_tokens_user_id"),
        "refresh_tokens",
        ["user_id"],
        unique=False,
    )
    op.create_table(
        "token_blacklists",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("token", sa.Text(), nullable=False),
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_token_blacklists_created_at"),
        "token_blacklists",
        ["created_at"],
        unique=False,
    )
    op.create_index(
        op.f("ix_token_blacklists_deleted_at"),
        "token_blacklists",
        ["deleted_at"],
        unique=False,
    )
    op.create_index(
        op.f("ix_token_blacklists_token"),
        "token_blacklists",
        ["token"],
        unique=True,
    )
    op.create_index(
        op.f("ix_token_blacklists_updated_at"),
        "token_blacklists",
        ["updated_at"],
        unique=False,
    )
    op.create_index(
        op.f("ix_token_blacklists_user_id"),
        "token_blacklists",
        ["user_id"],
        unique=False,
    )
    op.create_table(
        "user_store_auth_groups",
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("store_id", sa.BigInteger(), nullable=False),
        sa.Column("auth_group_id", sa.BigInteger(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["auth_group_id"],
            ["auth_groups.id"],
        ),
        sa.ForeignKeyConstraint(
            ["store_id"],
            ["stores.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("user_id", "store_id", "auth_group_id"),
    )
    op.create_index(
        op.f("ix_user_store_auth_groups_created_at"),
        "user_store_auth_groups",
        ["created_at"],
        unique=False,
    )
    op.create_index(
        op.f("ix_user_store_auth_groups_deleted_at"),
        "user_store_auth_groups",
        ["deleted_at"],
        unique=False,
    )
    op.create_index(
        op.f("ix_user_store_auth_groups_updated_at"),
        "user_store_auth_groups",
        ["updated_at"],
        unique=False,
    )
    op.create_table(
        "user_store_permissions",
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("store_id", sa.BigInteger(), nullable=False),
        sa.Column("permission_id", sa.BigInteger(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["permission_id"],
            ["mt_permissions.id"],
        ),
        sa.ForeignKeyConstraint(
            ["store_id"],
            ["stores.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("user_id", "store_id", "permission_id"),
    )
    op.create_index(
        op.f("ix_user_store_permissions_created_at"),
        "user_store_permissions",
        ["created_at"],
        unique=False,
    )
    op.create_index(
        op.f("ix_user_store_permissions_deleted_at"),
        "user_store_permissions",
        ["deleted_at"],
        unique=False,
    )
    op.create_index(
        op.f("ix_user_store_permissions_updated_at"),
        "user_store_permissions",
        ["updated_at"],
        unique=False,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(
        op.f("ix_user_store_permissions_updated_at"),
        table_name="user_store_permissions",
    )
    op.drop_index(
        op.f("ix_user_store_permissions_deleted_at"),
        table_name="user_store_permissions",
    )
    op.drop_index(
        op.f("ix_user_store_permissions_created_at"),
        table_name="user_store_permissions",
    )
    op.drop_table("user_store_permissions")
    op.drop_index(
        op.f("ix_user_store_auth_groups_updated_at"),
        table_name="user_store_auth_groups",
    )
    op.drop_index(
        op.f("ix_user_store_auth_groups_deleted_at"),
        table_name="user_store_auth_groups",
    )
    op.drop_index(
        op.f("ix_user_store_auth_groups_created_at"),
        table_name="user_store_auth_groups",
    )
    op.drop_table("user_store_auth_groups")
    op.drop_index(
        op.f("ix_token_blacklists_user_id"), table_name="token_blacklists"
    )
    op.drop_index(
        op.f("ix_token_blacklists_updated_at"), table_name="token_blacklists"
    )
    op.drop_index(
        op.f("ix_token_blacklists_token"), table_name="token_blacklists"
    )
    op.drop_index(
        op.f("ix_token_blacklists_deleted_at"), table_name="token_blacklists"
    )
    op.drop_index(
        op.f("ix_token_blacklists_created_at"), table_name="token_blacklists"
    )
    op.drop_table("token_blacklists")
    op.drop_index(
        op.f("ix_refresh_tokens_user_id"), table_name="refresh_tokens"
    )
    op.drop_index(
        op.f("ix_refresh_tokens_updated_at"), table_name="refresh_tokens"
    )
    op.drop_index(op.f("ix_refresh_tokens_token"), table_name="refresh_tokens")
    op.drop_index(op.f("ix_refresh_tokens_id"), table_name="refresh_tokens")
    op.drop_index(
        op.f("ix_refresh_tokens_deleted_at"), table_name="refresh_tokens"
    )
    op.drop_index(
        op.f("ix_refresh_tokens_created_at"), table_name="refresh_tokens"
    )
    op.drop_index(
        op.f("ix_refresh_tokens_access_token_jti"), table_name="refresh_tokens"
    )
    op.drop_table("refresh_tokens")
    op.drop_index(op.f("ix_users_username"), table_name="users")
    op.drop_index(op.f("ix_users_updated_at"), table_name="users")
    op.drop_index(op.f("ix_users_last_name_kana"), table_name="users")
    op.drop_index(op.f("ix_users_id"), table_name="users")
    op.drop_index(op.f("ix_users_first_name_kana"), table_name="users")
    op.drop_index(op.f("ix_users_deleted_at"), table_name="users")
    op.drop_index(op.f("ix_users_created_at"), table_name="users")
    op.drop_table("users")
    op.drop_index(op.f("ix_stores_updated_at"), table_name="stores")
    op.drop_index(op.f("ix_stores_id"), table_name="stores")
    op.drop_index(op.f("ix_stores_full_name"), table_name="stores")
    op.drop_index(op.f("ix_stores_deleted_at"), table_name="stores")
    op.drop_index(op.f("ix_stores_created_at"), table_name="stores")
    op.drop_table("stores")
    op.drop_index(
        op.f("ix_auth_group_permissions_updated_at"),
        table_name="auth_group_permissions",
    )
    op.drop_index(
        op.f("ix_auth_group_permissions_deleted_at"),
        table_name="auth_group_permissions",
    )
    op.drop_index(
        op.f("ix_auth_group_permissions_created_at"),
        table_name="auth_group_permissions",
    )
    op.drop_table("auth_group_permissions")
    op.drop_index(
        op.f("ix_mt_permissions_updated_at"), table_name="mt_permissions"
    )
    op.drop_index(op.f("ix_mt_permissions_id"), table_name="mt_permissions")
    op.drop_index(
        op.f("ix_mt_permissions_deleted_at"), table_name="mt_permissions"
    )
    op.drop_index(
        op.f("ix_mt_permissions_created_at"), table_name="mt_permissions"
    )
    op.drop_index(op.f("ix_mt_permissions_code"), table_name="mt_permissions")
    op.drop_table("mt_permissions")
    op.drop_index(op.f("ix_cities_updated_at"), table_name="cities")
    op.drop_index(op.f("ix_cities_id"), table_name="cities")
    op.drop_index(op.f("ix_cities_deleted_at"), table_name="cities")
    op.drop_index(op.f("ix_cities_created_at"), table_name="cities")
    op.drop_table("cities")
    op.drop_index(op.f("ix_auth_groups_updated_at"), table_name="auth_groups")
    op.drop_index(op.f("ix_auth_groups_name"), table_name="auth_groups")
    op.drop_index(op.f("ix_auth_groups_id"), table_name="auth_groups")
    op.drop_index(op.f("ix_auth_groups_deleted_at"), table_name="auth_groups")
    op.drop_index(op.f("ix_auth_groups_created_at"), table_name="auth_groups")
    op.drop_table("auth_groups")
    # ### end Alembic commands ###
