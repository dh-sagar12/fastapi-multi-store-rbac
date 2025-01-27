from libs.shared.utils.base_crud import CRUDBase
from services.src_auth.app.models.auth_group import AuthGroup
from services.src_auth.app.schemas.auth_group import CreateAuthGroup


class AuthGroupService(CRUDBase[AuthGroup, CreateAuthGroup, CreateAuthGroup]):
    pass
