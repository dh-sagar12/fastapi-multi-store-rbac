from fastapi import Depends, FastAPI

from fastapi.middleware.cors import CORSMiddleware
from libs.shared.auth.jwt_validator import JWTBearer
from services.src_auth.app.api.user import router as user_router
from services.src_auth.app.api.user import open_router as user_open_router
from services.src_auth.app.api.store import router as store_router
from services.src_auth.app.api.auth_group import router as auth_group_router
from services.src_auth.app.api.permission import router as permission_router


app = FastAPI(
    title="HamroMart- SmartMart Management System",
    version="1.0",
    servers=[{"url": "http://localhost:8001"}],
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(user_router, dependencies=[Depends(JWTBearer())])
app.include_router(user_open_router)
app.include_router(store_router, dependencies=[Depends(JWTBearer())])
app.include_router(auth_group_router, dependencies=[Depends(JWTBearer())])
app.include_router(permission_router, dependencies=[Depends(JWTBearer())])


@app.get("/health")
def health_check():
    return {"status": "healthy"}
