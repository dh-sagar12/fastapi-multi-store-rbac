from typing import List
from fastapi import APIRouter, Depends, HTTPException, Path
from libs.shared.auth.permission_checker import has_permission
from libs.shared.db.database import get_db, get_db_ro
from libs.shared.utils.custom_exception import ServiceException
from libs.shared.utils.sucess_response import ResponseModel, Status
from services.src_auth.app.crud.permission_service import PermissionService
from services.src_auth.app.models import Permission
from services.src_auth.app.schemas.permission import (
    CreatePermission,
    GetPermission,
)
from sqlalchemy.orm import Session


router = APIRouter(prefix="/permissions", tags=["Permission"])


@router.post(
    "/create",
    dependencies=[has_permission(["mt_permissions.create"])],
    response_model=ResponseModel,
)
async def create_permission(
    request_body: CreatePermission,
    db: Session = Depends(get_db),
):
    try:
        service = PermissionService(model=Permission, db=db)
        service.create(obj_in=request_body, auto_commit=True)
        return ResponseModel(
            status=Status.Success, message="Permission Created Successfully"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "",
    dependencies=[has_permission(["mt_permissions.view"])],
    response_model=List[GetPermission],
)
async def get_all_permissions(
    db: Session = Depends(get_db_ro),
):
    try:
        service = PermissionService(model=Permission, db=db)
        data = service.get_multi()
        return [
            GetPermission(
                id=item.id,
                name=item.name,
                code=item.code,
            )
            for item in data
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/update/{id}",
    dependencies=[has_permission(["mt_permissions.update"])],
    response_model=ResponseModel,
)
async def update_permission(
    request_body: CreatePermission,
    id: int = Path(...),
    db: Session = Depends(get_db),
):
    try:
        service = PermissionService(model=Permission, db=db)
        service.update(
            db_obj=service.get(id=id), obj_in=request_body, auto_commit=True
        )
        return ResponseModel(
            status=Status.Success, message="Permission Updated Successfully"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/assign-permissions-to-group",
    dependencies=[
        has_permission(
            [
                "auth_group_permissions.update",
                "auth_group_permissions.create",
                "auth_group_permissions.delete",
            ]
        )
    ],
)
async def assign_permissions_to_group(
    auth_group_id: int,
    permission_ids: List[int],
    db: Session = Depends(get_db),
):
    try:
        service = PermissionService(model=Permission, db=db)
        service.assign_permission_to_auth_group(
            auth_group_id=auth_group_id, permission_ids=permission_ids
        )

    except ServiceException as e:
        db.rollback()
        raise HTTPException(status_code=e.status_code, detail=e.message)

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/assign-permissions-to-user",
    response_model=ResponseModel,
    dependencies=[
        has_permission(
            [
                "user_store_permissions.update",
                "user_store_permissions.create",
                "user_store_permissions.delete",
            ]
        )
    ],
)
async def assign_permissions_to_users(
    user_id: int,
    store_id: int,
    permission_ids: List[int],
    db: Session = Depends(get_db),
):
    try:
        service = PermissionService(model=Permission, db=db)
        service.assign_permission_to_users(
            user_id=user_id, store_id=store_id, permission_ids=permission_ids
        )

    except ServiceException as e:
        db.rollback()
        raise HTTPException(status_code=e.status_code, detail=e.message)

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
