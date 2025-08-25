from app.models.warehouse import Warehouse, WarehouseCreate, WarehouseUpdate
from .base import MongoCRUD

warehouse_service = MongoCRUD(collection="warehouses", model_cls=Warehouse, create_cls=WarehouseCreate, update_cls=WarehouseUpdate)
