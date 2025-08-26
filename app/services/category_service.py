from app.models.category import Category, CategoryCreate, CategoryUpdate
from .base import MongoCRUD


class CategoryService(MongoCRUD):
    def __init__(self):
        super().__init__(
            collection="categories",
            model_cls=Category,
            create_cls=CategoryCreate,
            update_cls=CategoryUpdate
        )

    async def create(self, payload: CategoryCreate) -> Category:
        # ✅ بررسی parent_id
        if payload.parent_id:
            parent = await self.get(payload.parent_id)
            if not parent:
                raise ValueError(f"Parent category with id {payload.parent_id} does not exist")

        return await super().create(payload)

    async def update(self, id_, patch: CategoryUpdate) -> Category | None:
        if patch.parent_id:
            parent = await self.get(patch.parent_id)
            if not parent:
                raise ValueError(f"Parent category with id {patch.parent_id} does not exist")

        return await super().update(id_, patch)


category_service = CategoryService()
