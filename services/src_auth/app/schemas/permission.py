from pydantic import BaseModel


class CreatePermission(BaseModel):
    name: str
    code: str


class GetPermission(CreatePermission):
    id: int
