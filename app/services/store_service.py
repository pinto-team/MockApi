from app.models.store import Store, StoreCreate, StoreUpdate
from .base import MongoCRUD

store_service = MongoCRUD(collection="stores", model_cls=Store, create_cls=StoreCreate, update_cls=StoreUpdate)
