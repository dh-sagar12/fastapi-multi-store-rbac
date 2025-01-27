from pydantic import BaseModel


class CreateAuthGroup(BaseModel):
    name: str


class GetAuthGroup(CreateAuthGroup):
    id: int
