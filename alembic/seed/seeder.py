import json
import sys

from sqlalchemy import func, insert
from sqlalchemy.orm import Session

from libs.shared.db.database import get_db
from libs.shared.utils.logger import logger
from services.src_auth.app.core.hash_password import hash_password
from services.src_auth.app.models.auth_group_permission import (
    auth_group_permissions,
)
from services.src_auth.app.models.permission import Permission
from services.src_auth.app.models.user_store_auth_group import (
    user_store_auth_groups,
)
from services.src_auth.app.models.auth_group import AuthGroup
from services.src_auth.app.models.city import City
from services.src_auth.app.models.store import Store
from services.src_auth.app.models.user import User


sys.path.append("/app")


def seed_cities(db: Session):
    logger.info("SEED: Inserting Cities Data....")
    with open("/app/alembic/seed/master/cities.json") as file:
        cities = json.load(file)
        city_obj = [
            City(
                id=city["id"],
                name=city["name"],
                postal_code=city["postal_code"],
            )
            for city in cities
        ]
        db.add_all(city_obj)
        db.flush()


def seed_stores(db: Session):
    logger.info("SEED: Inserting Stores Data....")
    with open("/app/alembic/seed/master/stores.json") as file:
        stores_data = json.load(file)
        store_objs = [
            Store(
                id=store.get("id"),
                name=store.get("name"),
                full_name=store.get("full_name"),
                postal_code=store.get("postal_code"),
                phone_number=store.get("phone_number"),
                city_id=store.get("city_id"),
                prefecture=store.get("prefecture"),
                street=store.get("street"),
                building_name=store.get("building_name"),
            )
            for store in stores_data
        ]
        db.add_all(store_objs)
        db.flush()


def seed_auth_groups(db: Session):
    logger.info("SEED: Inserting Auth Groups Data....")
    with open("/app/alembic/seed/master/auth_groups.json") as file:
        auth_groups_data = json.load(file)

        auth_group_objs = [
            AuthGroup(
                id=group.get("id"),
                name=group.get("name"),
            )
            for group in auth_groups_data
        ]

        db.add_all(auth_group_objs)
        db.flush()


def seed_users(db: Session):
    logger.info("SEED: Inserting Users Data....")
    with open("/app/alembic/seed/master/users.json") as file:
        users = json.load(file)

        for user in users:
            user_obj = {
                "id": user.get("id"),
                "username": user.get("username"),
                "first_name": user.get("first_name"),
                "last_name": user.get("last_name"),
                "first_name_kana": user.get("first_name_kana"),
                "last_name_kana": user.get("last_name_kana"),
                "password": hash_password(user.get("password")),
                "primary_store_id": user.get("primary_store_id"),
            }
            user_obj = User(**user_obj)
            db.add(user_obj)
            db.flush()
            auth_groups = [
                {
                    "user_id": user_obj.id,
                    "store_id": group.get("store_id"),
                    "auth_group_id": group.get("auth_group_id"),
                }
                for group in user.get("auth_groups")
            ]
            stmt = user_store_auth_groups.insert().values(auth_groups)
            db.execute(stmt)
            db.flush()


def add_permission_to_admin(db: Session):
    logger.info("SEED: Assigning All Permission to Admin Group....")
    auth_group = db.query(AuthGroup).filter_by(name="Admin").first()
    permission_ids = []
    for permission in db.query(Permission).all():
        permission_ids.append(permission.id)

    if permission_ids:
        values = [
            {
                "auth_group_id": auth_group.id,
                "permission_id": permission.id,
                "created_at": func.now(),
                "updated_at": func.now(),
                "deleted_at": None,
            }
            for permission in db.query(Permission).all()
        ]

        stmt = insert(auth_group_permissions).values(values)

        db.execute(stmt)


def seed_master_data():
    db = next(get_db())
    try:
        seed_cities(db=db)
        seed_stores(db=db)
        seed_auth_groups(db=db)
        seed_users(db=db)
        add_permission_to_admin(db=db)
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.commit()
