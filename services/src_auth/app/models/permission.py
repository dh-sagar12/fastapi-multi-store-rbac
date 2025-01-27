from sqlalchemy import Column, String
from libs.shared.utils.base_model import BaseModel


class Permission(BaseModel):
    __tablename__ = "mt_permissions"
    
    name = Column(String(255), nullable=False)  
    code = Column(String(255), nullable=False, unique=True, index=True)
