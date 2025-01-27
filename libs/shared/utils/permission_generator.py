from sqlalchemy import create_engine, inspect
from libs.shared.db.database import Base, get_db
from libs.shared.utils.logger import logger
from services.src_auth.app.models.permission import Permission


class PermissionCreator:
    def __init__(self, db_url):
        self.db = next(get_db())
        self.engine = create_engine(db_url)

    def get_all_model_names(self):
        """Get all model names from Base.metadata"""
        return [table.name for table in Base.metadata.sorted_tables]

    def create_crud_permissions(self, models):
        """Create CRUD permissions for all models"""
        try:
            inspector = inspect(self.engine)
            existing_tables = inspector.get_table_names()

            # Only proceed if permissions table exists
            if "mt_permissions" not in existing_tables:
                logger.warning("Permissions table does not exist yet")
                return

            # Get existing permissions to avoid duplicates
            existing_permissions = self.db.query(Permission).all()
            existing_permission_names = {p.code for p in existing_permissions}
            # CRUD actions
            CRUD_ACTIONS = ["create", "view", "update", "delete"]

            # Generate permissions for each model
            new_permissions = []
            for model in models:
                for action in CRUD_ACTIONS:
                    code = f"{model.lower()}.{action}"
                    name = f"Can {action.capitalize()} {model.lower()}"
                    if code not in existing_permission_names:
                        new_permission = Permission(
                            name=name,
                            code=code,
                        )
                        new_permissions.append(new_permission)
                        self.db.add(new_permission)

            if new_permissions:
                logger.info(f"Creating {len(new_permissions)} new permissions")
                self.db.commit()

        except Exception as e:
            logger.error(f"Error creating permissions: {str(e)}")
            self.db.rollback()
            raise
        finally:
            self.db.close()

    def get_pending_permissions(self, target_models=None):
        """Get list of permissions that would be created without actually creating them."""
        try:
            existing_permissions = self.db.query(Permission).all()
            existing_permission_names = {p.code for p in existing_permissions}

            models = target_models or self.get_all_model_names()
            CRUD_ACTIONS = ["create", "view", "update", "delete"]

            pending_permissions = []
            for model in models:
                for action in CRUD_ACTIONS:
                    code = f"{model.lower()}.{action}"
                    name = f"Can {action.capitalize()} {model.lower()}"
                    if code not in existing_permission_names:
                        pending_permissions.append(
                            {
                                "name": name,
                                "code": code,
                            }
                        )
            return pending_permissions
        finally:
            self.db.close()

    def list_permissions(self):
        """List all existing permissions."""
        try:
            return self.db.query(Permission).all()
        finally:
            self.db.close()
