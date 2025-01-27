from typing import List
from libs.shared.auth.permission_checker import has_permission
from libs.shared.utils.sucess_response import ResponseModel, Status
from services.src_auth.app.schemas.auth_group import (
    CreateAuthGroup,
    GetAuthGroup,
)
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, APIRouter, Path
from libs.shared.db.database import get_db, get_db_ro
from services.src_auth.app.crud.auth_group_service import AuthGroupService
from services.src_auth.app.models.auth_group import AuthGroup


router = APIRouter(prefix="/auth-group", tags=["Auth Group"])


@router.post("/create", dependencies=[has_permission(["auth_groups.create"])])
async def create_auth_group(
    request_body: CreateAuthGroup,
    db: Session = Depends(get_db),
):
    try:
        service = AuthGroupService(model=AuthGroup, db=db)
        service.create(obj_in=request_body, auto_commit=True)
        return ResponseModel(
            status=Status.Success, message="Auth Group Created Successfully"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "",
    dependencies=[has_permission(["auth_groups.view"])],
    response_model=List[GetAuthGroup],
)
async def get_all_permissions(
    db: Session = Depends(get_db_ro),
):
    try:
        service = AuthGroupService(model=AuthGroup, db=db)
        data = service.get_multi()
        return [
            GetAuthGroup(
                id=item.id,
                name=item.name,
            )
            for item in data
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/update/{id}",
    dependencies=[has_permission(["auth_groups.update"])],
    response_model=ResponseModel,
)
async def update_auth_group(
    request_body: CreateAuthGroup,
    id: int = Path(...),
    db: Session = Depends(get_db),
):
    try:
        service = AuthGroupService(model=AuthGroup, db=db)
        service.update(
            db_obj=service.get(id=id), obj_in=request_body, auto_commit=True
        )
        return ResponseModel(
            status=Status.Success, message="Auth Group Updated Successfully"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
