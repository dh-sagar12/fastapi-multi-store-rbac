from enum import Enum
from typing import Generic, TypeVar
from pydantic import BaseModel

T = TypeVar("T")


class Status(Enum):
    Success = "SUCCESS"
    Failed = "FAILED"


class ResponseModel(BaseModel, Generic[T]):
    status: Status
    message: str
