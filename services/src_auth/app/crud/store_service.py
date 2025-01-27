from typing import List
from libs.shared.utils.base_crud import CRUDBase
from services.src_auth.app.models.store import Store
from services.src_auth.app.schemas.store import CreateStore


class StoreService(CRUDBase[Store, CreateStore, CreateStore]):
    


    def get_filtered_stores(self, store_ids: List[int]):
        self.db
