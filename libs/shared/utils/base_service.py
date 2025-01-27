from abc import ABC, abstractmethod
from sqlalchemy.orm import Session


class BaseServiceABC(ABC):
    def __init__(self, db: Session, payload) -> None:
        self.db = db
        self.payload = payload

    def start(self) -> None:
        self._run()

    def _run(self) -> None:
        self._execute()

    @abstractmethod
    def _execute(self):
        raise NotImplementedError
