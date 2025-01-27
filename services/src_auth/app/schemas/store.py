from typing import Union
from pydantic import BaseModel


class CreateStore(BaseModel):
    name: str
    full_name: str
    postal_code: Union[str, None]
    phone_number: Union[str, None]
    city_id: int
    prefecture: Union[str, None]
    street: Union[str, None]
    building_name: Union[str, None]


class GetStore(CreateStore):
    id: int
