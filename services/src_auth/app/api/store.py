from typing import List
from fastapi import APIRouter, Depends, HTTPException, Path
from libs.shared.auth.permission_checker import has_permission
from libs.shared.db.database import get_db
from libs.shared.utils.sucess_response import ResponseModel, Status
from services.src_auth.app.crud.store_service import StoreService
from services.src_auth.app.models.store import Store
from services.src_auth.app.schemas.store import CreateStore, GetStore
from sqlalchemy.orm import Session


router = APIRouter(prefix="/stores", tags=["Store"])


@router.post(
    "/create",
    dependencies=[has_permission(["stores.create"])],
    response_model=ResponseModel,
)
async def create_store(
    request_body: CreateStore,
    db: Session = Depends(get_db),
):
    try:
        service = StoreService(model=Store, db=db)
        service.create(obj_in=request_body, auto_commit=True)
        return ResponseModel(
            status=Status.Success, message="Store Created Successfully"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "",
    dependencies=[has_permission(["stores.view"])],
    response_model=List[GetStore],
)
async def get_all_store(
    db: Session = Depends(get_db),
    offset: int = 0,
    limit: int = 100,
    store_ids: List[int] = [],
):
    try:
        service = StoreService(model=Store, db=db)
        filters  =  {
            "id": {"in": store_ids}
        }
        data = service.get_multi(skip=offset, limit=limit, filters=filters)
        return [
            GetStore(
                id=item.id,
                name=item.name,
                full_name=item.full_name,
                postal_code=item.postal_code,
                phone_number=item.phone_number,
                city_id=item.city_id,
                prefecture=item.prefecture,
                street=item.street,
                building_name=item.building_name,
            )
            for item in data
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/update/{id}",
    dependencies=[has_permission(["stores.update"])],
    response_model=ResponseModel,
)
async def update_store(
    request_body: CreateStore,
    id: int = Path(...),
    db: Session = Depends(get_db),
):
    try:
        service = StoreService(model=Store, db=db)
        service.update(
            db_obj=service.get(id=id), obj_in=request_body, auto_commit=True
        )
        return ResponseModel(
            status=Status.Success, message="Store Updated Successfully"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
