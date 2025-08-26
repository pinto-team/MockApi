from app.models.warehouse import Warehouse, WarehouseCreate, WarehouseUpdate
from .base import MongoCRUD
# ❗ اگر مدل User یا Service مربوط به Manager داشتی اینجا ایمپورت کن
# from app.services.user_service import user_service


class WarehouseService(MongoCRUD):
    def __init__(self):
        super().__init__(
            collection="warehouses",
            model_cls=Warehouse,
            create_cls=WarehouseCreate,
            update_cls=WarehouseUpdate
        )

    async def create(self, payload: WarehouseCreate) -> Warehouse:
        # ✅ بررسی manager_id (اگر وجود داشته باشد)
        if payload.manager_id:
            # manager = await user_service.get(payload.manager_id)
            # if not manager:
            #     raise ValueError(f"Manager with id {payload.manager_id} does not exist")
            pass

        return await super().create(payload)

    async def update(self, id_, patch: WarehouseUpdate) -> Warehouse | None:
        if patch.manager_id:
            # manager = await user_service.get(patch.manager_id)
            # if not manager:
            #     raise ValueError(f"Manager with id {patch.manager_id} does not exist")
            pass

        return await super().update(id_, patch)


warehouse_service = WarehouseService()
