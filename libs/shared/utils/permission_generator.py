from typing import List
from sqlalchemy.orm import relationship, Session

from libs.shared.db.database import Base
from services.src_auth.app.models.permission import Permission


class PermissionGenerator:
    """
    Permission generator for models with automatic CRUD permissions
    """
    CRUD_ACTIONS = ['create', 'view', 'update', 'delete']
    
    @classmethod
    def generate_model_permissions(cls, model_name: str) -> List[dict]:
        """Generate CRUD permissions for a model"""
        permissions = []
        for action in cls.CRUD_ACTIONS:
            code = f"{model_name.lower()}.{action}"
            name = f"Can {action} {model_name.lower()}"
            permissions.append({
                "code": code,
                "name": name
            })
        return permissions


def create_permission_migration(connection, **kw):
    """
    Alembic operation to create permissions for new models
    """

    session = Session(bind=connection)
    
    # Get all models that inherit from Base
    for model in Base.metadata.tables.keys():
        perms = PermissionGenerator.generate_model_permissions(model)
        
        # Create permissions if they don't exist
        for perm in perms:
            existing = session.query(Permission).filter_by(code=perm['code']).first()
            if not existing:
                new_perm = Permission(**perm)
                session.add(new_perm)
    
    session.commit()
