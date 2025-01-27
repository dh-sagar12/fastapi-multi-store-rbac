from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials

from libs.shared.auth.get_current_user import get_current_user
from libs.shared.auth.get_token_data import get_payload_data
from libs.shared.auth.jwt_validator import JWTBearer
from libs.shared.auth.permission_checker import has_permission
from libs.shared.db.database import get_db, get_db_ro
from libs.shared.utils.custom_exception import ServiceException
from libs.shared.utils.sucess_response import ResponseModel, Status
from services.src_auth.app.crud.user_service import UserService
from services.src_auth.app.models.user import User
from services.src_auth.app.schemas.jwt_payload import JWTPayload
from services.src_auth.app.schemas.users import (
    ChangePassword,
    CreatUserPayload,
    CurrentUser,
    GetUser,
    Login,
    LoginSucess,
)
from sqlalchemy.orm import Session


# protected route with JWTBearer()
router = APIRouter(tags=["User"])

open_router = APIRouter(tags=["User"])


@router.post(
    "/users",
    dependencies=[has_permission(["users.create"])],
    response_model=ResponseModel,
    description="Create new user",
)
async def create_user(
    request_body: CreatUserPayload,
    db: Session = Depends(get_db),
):
    try:
        service = UserService(model=User, db=db)
        service.create_new_user(obj_in=request_body)
        return ResponseModel(
            status=Status.Success, message="User Created Successfully"
        )

    except ServiceException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/users",
    dependencies=[has_permission(["users.view"])],
    response_model=List[GetUser],
    description="Get list of active users available",
)
async def get_users(db: Session = Depends(get_db_ro)):
    try:
        service = UserService(model=User, db=db)
        users = service.get_multi()
        return [
            GetUser(
                id=item.id,
                first_name=item.first_name,
                last_name=item.last_name,
                first_name_kana=item.first_name_kana,
                last_name_kana=item.last_name_kana,
                username=item.username,
                primary_store=item.primary_store.name,
            )
            for item in users
        ]
    except ServiceException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/auth/me",
    response_model=CurrentUser,
    description="Get the information about the current user, its associated stores and permissions",
)
async def get_me(
    payload: JWTPayload = Depends(get_payload_data),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db_ro),
):
    try:

        service = UserService(model=User, db=db)
        return service.get_me(user=user, payload=payload)
    except ServiceException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@open_router.post(
    "/login",
    response_model=LoginSucess,
    description="Input credential and get access and refresh token if the user's credential is valid",
)
async def login(
    request_body: Login,
    db: Session = Depends(get_db),
):
    try:
        service = UserService(model=User, db=db)
        data = service.login(obj_in=request_body)
        return data

    except ServiceException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/change-password",
    response_model=ResponseModel,
    description="Change the current password with the help of current password",
)
async def change_password(
    request_body: ChangePassword,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    try:
        service = UserService(model=User, db=db)
        data = service.change_password(obj_in=request_body, user=user)
        return data

    except ServiceException as e:
        db.rollback()
        raise HTTPException(status_code=e.status_code, detail=e.message)

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/logout",
    response_model=ResponseModel,
    description="Logout the current user",
)
async def logout(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
    payload: JWTPayload = Depends(get_payload_data),
    token: Optional[HTTPAuthorizationCredentials] = Depends(JWTBearer()),
):
    try:
        service = UserService(model=User, db=db)
        data = service.logout(user=user, payload=payload, token=token)
        return data

    except ServiceException as e:
        db.rollback()
        raise HTTPException(status_code=e.status_code, detail=e.message)

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@open_router.post(
    "/get-access-token",
    response_model=LoginSucess,
    description="Get access_token and refresh_token from refresh_token we have",
)
async def get_access_token(
    refresh_token: str,
    db: Session = Depends(get_db),
):
    try:
        service = UserService(model=User, db=db)
        data = service.get_access_token(refresh_token=refresh_token)
        return data
    except ServiceException as e:
        db.rollback()
        raise HTTPException(status_code=e.status_code, detail=e.message)

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/switch-store",
    response_model=LoginSucess,
    description="Switch loggedin store to another store.",
)
async def switch_store(
    store_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
    token: Optional[HTTPAuthorizationCredentials] = Depends(JWTBearer()),
    payload: JWTPayload = Depends(get_payload_data),
):
    try:
        service = UserService(model=User, db=db)
        data = service.switch_store(
            store_id=store_id, user=user, token=token, payload=payload
        )
        return data
    except ServiceException as e:
        db.rollback()
        raise HTTPException(status_code=e.status_code, detail=e.message)

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
