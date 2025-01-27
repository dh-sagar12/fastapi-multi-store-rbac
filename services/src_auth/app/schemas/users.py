from typing import List, Optional
from pydantic import BaseModel, Field


class StoreAuthGroups(BaseModel):
    store_id: Optional[int] = Field(None, example=1, title="store_id")
    auth_group_id: Optional[int] = Field(
        None, example=1, title="auth_group_id"
    )


class CreatUserPayload(BaseModel):
    username: str = Field(..., example="user123", title="username")
    first_name: str = Field(None, example="first_name", title="first_name")
    last_name: str = Field(None, example="last_name", title="last_name")
    first_name_kana: str = Field(
        None, example="firstname", title="first_name_kana"
    )
    password: str = Field(None, example="password", title="password")
    last_name_kana: str = Field(
        None, example="lastname", title="last_name_kana"
    )
    primary_store_id: int = Field(None, example=1, title="primary_store_id")
    store_groups: List[StoreAuthGroups] = Field(..., title="store_groups")


class Login(BaseModel):
    username: str
    password: str


class LoginSucess(BaseModel):
    access_token: str
    refresh_token: str


class ChangePassword(BaseModel):
    current_password: str
    new_password: str


class CurrentUser(BaseModel):
    id: int
    username: str
    first_name: str
    last_name: str
    first_name_kana: str
    last_name_kana: str
    primary_store_id: int
    stores: List[int]
    auth_group: int
    permissions: List[str]


class GetUser(BaseModel):
    id: int
    username: str
    first_name: str
    last_name: str
    first_name_kana: str
    last_name_kana: str
    primary_store: str
