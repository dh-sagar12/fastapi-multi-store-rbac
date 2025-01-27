from typing import Optional, Tuple
from sqlalchemy import func
from libs.shared.utils.base_crud import CRUDBase
from libs.shared.utils.custom_exception import ServiceException
from libs.shared.utils.sucess_response import ResponseModel, Status
from services.src_auth.app.core.decode_tokens import decode_refresh_token
from services.src_auth.app.core.encode_tokens import (
    encode_access_token,
    encode_refresh_token,
)
from services.src_auth.app.core.get_jti import get_jti
from services.src_auth.app.core.get_user_auth_group import get_user_auth_group
from services.src_auth.app.core.get_user_permission_roles import (
    get_role_and_user_permissions,
)
from services.src_auth.app.core.hash_password import hash_password
from services.src_auth.app.core.verify_password import verify_password
from services.src_auth.app.models.refresh_token import RefreshToken
from services.src_auth.app.models.token_blacklist import TokenBlacklist
from services.src_auth.app.models.user_store_auth_group import (
    user_store_auth_groups,
)
from services.src_auth.app.models.user import User
from services.src_auth.app.schemas.jwt_payload import JWTPayload
from services.src_auth.app.schemas.users import (
    ChangePassword,
    CreatUserPayload,
    CurrentUser,
    Login,
    LoginSucess,
)
from fastapi import status


class UserService(CRUDBase[User, CreatUserPayload, CreatUserPayload]):

    def create_new_user(self, obj_in: CreatUserPayload):

        user_obj = {
            "username": obj_in.username,
            "first_name": obj_in.first_name,
            "last_name": obj_in.last_name,
            "first_name_kana": obj_in.first_name_kana,
            "last_name_kana": obj_in.last_name_kana,
            "password": hash_password(obj_in.password),
            "primary_store_id": obj_in.primary_store_id,
        }
        user = self.create(obj_in=user_obj, auto_commit=False)
        auth_groups = [
            {
                "user_id": user.id,
                "store_id": group.store_id,
                "auth_group_id": group.auth_group_id,
            }
            for group in obj_in.store_groups
        ]
        stmt = user_store_auth_groups.insert().values(auth_groups)
        self.db.execute(stmt)
        self.db.commit()
        return user

    def get_tokens(
        self,
        user: User,
        store_id: Optional[int] = None,
    ) -> Tuple[str, str]:

        store_id = store_id if store_id else user.primary_store_id

        auth_group_id = get_user_auth_group(
            user_id=user.id,
            store_id=store_id,
            db=self.db,
        ).get("auth_group_id")

        if not auth_group_id:
            raise ServiceException(
                message="Invalid Role",
                status_code=status.HTTP_401_UNAUTHORIZED,
            )

        jti = get_jti()
        access_token = encode_access_token(
            user=user,
            auth_group_id=auth_group_id,
            store_id=store_id,
            jti=jti,
        )

        refresh_token = encode_refresh_token(
            user=user,
            auth_group_id=auth_group_id,
            store_id=store_id,
            access_token_jti=jti,
            db=self.db,
        )
        return access_token, refresh_token

    def login(self, obj_in: Login):
        user = self.db.query(User).filter_by(username=obj_in.username).first()
        if not user:
            raise ServiceException(status_code=404, message="User Not Found")

        is_password_verified = verify_password(obj_in.password, user.password)
        if not is_password_verified:
            raise ServiceException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                message="Invalid Password!!",
            )

        access_token, refresh_token = self.get_tokens(user=user)
        user.last_logged_in = func.now()
        self.db.commit()
        return LoginSucess(
            access_token=access_token, refresh_token=refresh_token
        )

    def change_password(
        self, obj_in: ChangePassword, user: User
    ) -> ResponseModel:
        is_password_verified = verify_password(
            obj_in.current_password, user.password
        )
        if not is_password_verified:
            raise ServiceException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                message="Invalid Password !!",
            )

        user.password = hash_password(obj_in.new_password)
        self.db.commit()
        return ResponseModel(
            status=Status.Success, message="Password Changed Successfully.!!"
        )

    def logout(self, user: User, payload: JWTPayload, token) -> ResponseModel:
        # while logout Refreshtoken and access token both should be blacklisted.

        refresh_token = (
            self.db.query(RefreshToken)
            .filter_by(
                user_id=user.id,
                access_token_jti=payload.jti,
            )
            .first()
        )
        if refresh_token:
            refresh_token.deleted_at = func.now()

        # add access token to the blacklisted as well

        blacklist = TokenBlacklist(token=token, user_id=user.id)
        self.db.add(blacklist)
        self.db.commit()
        return ResponseModel(
            status=Status.Success, message="Logout Sucessfully!!"
        )

    def get_access_token(self, refresh_token: str):
        """Issue new access and refresh token from the available refresh_token and blacklist previous access and refresh"""

        # check whether the token is valid or not
        data = decode_refresh_token(refresh_token)

        if data:
            # since token is valid now procced to blacklist and issue new tokens

            refresh_token = (
                self.db.query(RefreshToken)
                .filter_by(token=refresh_token)
                .first()
            )
            if not refresh_token:
                raise ServiceException(
                    message="Invalid Token",
                    status_code=status.HTTP_404_NOT_FOUND,
                )
            refresh_token.deleted_at = func.now()

            user = self.get(id=data.get("user_id"))
            access_token, refresh_token = self.get_tokens(user=user)
            return LoginSucess(
                access_token=access_token, refresh_token=refresh_token
            )

    def switch_store(
        self, store_id: int, user: User, token: str, payload: JWTPayload
    ):

        # first check whether the store_id provided has some auth_group for current user
        # if not store_id sent has some role for user then return

        stores = [store.id for store in user.stores]
        if store_id not in stores:
            raise ServiceException(
                message="Permission Denied",
                status_code=status.HTTP_403_FORBIDDEN,
            )

        # find refresh token associated with this session
        refresh_token = (
            self.db.query(RefreshToken)
            .filter_by(user_id=user.id, access_token_jti=payload.jti)
            .first()
        )
        if refresh_token:
            refresh_token.deleted_at = func.now()

        # add access token to blacklist list
        blacklist = TokenBlacklist(user_id=user.id, token=token)
        self.db.add(blacklist)

        access_token, refresh_token = self.get_tokens(
            user=user, store_id=store_id
        )
        return LoginSucess(
            access_token=access_token, refresh_token=refresh_token
        )

    def get_me(self, user: User, payload: JWTPayload):
        permissions = get_role_and_user_permissions(
            user_id=user.id,
            role_id=payload.auth_group_id,
            store_id=payload.store_id,
            db=self.db,
        )
        response = CurrentUser(
            id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            first_name_kana=user.first_name_kana,
            last_name_kana=user.last_name_kana,
            primary_store_id=user.primary_store_id,
            auth_group=payload.auth_group_id,
            stores=[store.id for store in user.stores],
            permissions=permissions,
        )

        return response
