from uuid import UUID
from typing import List, Optional
from pymongo import ASCENDING, DESCENDING

from .base import MongoCRUD, _serialize
from app.models.product import Product, ProductCreate, ProductUpdate, ProductResponse, WarehouseAvailabilityResponse
from app.models.store import Store
from app.models.category import Category
from app.models.brand import Brand
from app.models.warehouse import Warehouse
from app.models.image import Image
from app.db.mongo import db

class ProductService(MongoCRUD):
    def __init__(self):
        super().__init__(collection="products", model_cls=Product, create_cls=ProductCreate, update_cls=ProductUpdate)

    async def list(
        self,
        search: Optional[str] = None,
        sort_by_price: Optional[str] = None  # "asc" or "desc"
    ) -> List[ProductResponse]:
        query = {}

        # جستجو در name یا description یا tags
        if search:
            query = {
                "$or": [
                    {"name": {"$regex": search, "$options": "i"}},
                    {"full_name": {"$regex": search, "$options": "i"}},
                    {"description": {"$regex": search, "$options": "i"}},
                    {"tags": {"$regex": search, "$options": "i"}},
                ]
            }

        cursor = db[self.collection].find(query)

        # ترتیب بر اساس قیمت
        if sort_by_price:
            order = ASCENDING if sort_by_price == "asc" else DESCENDING
            cursor = cursor.sort("price", order)

        products = [self.model_cls(**_serialize(doc)) async for doc in cursor]
        return await self._populate(products)

    async def get(self, id_: UUID) -> ProductResponse | None:
        product = await super().get(id_)
        if not product:
            return None
        populated = await self._populate([product])
        return populated[0]

    async def _populate(self, products: List[Product]) -> List[ProductResponse]:
        responses: List[ProductResponse] = []
        for p in products:
            data = p.model_dump()

            # Store
            store_doc = await db["stores"].find_one({"_id": str(p.store_id)}) if hasattr(p, "store_id") else None
            if store_doc:
                data["store"] = Store(**_serialize(store_doc))

            # Category
            cat_doc = await db["categories"].find_one({"_id": str(p.category_id)})
            if cat_doc:
                data["category"] = Category(**_serialize(cat_doc))

            # Brand
            brand_doc = await db["brands"].find_one({"_id": str(p.brand_id)})
            if brand_doc:
                data["brand"] = Brand(**_serialize(brand_doc))

            # Warehouses
            wa_list = []
            for wa in getattr(p, "warehouse_availability", []) or []:
                wa_dict = wa.model_dump()
                w_doc = await db["warehouses"].find_one({"_id": str(wa.warehouse_id)})
                if w_doc:
                    wa_dict["warehouse"] = Warehouse(**_serialize(w_doc))
                wa_list.append(WarehouseAvailabilityResponse(**wa_dict))
            data["warehouse_availability"] = wa_list

            # Images
            imgs = []
            async for img_doc in db["images"].find({"product_id": str(p.id)}):
                imgs.append(Image(**_serialize(img_doc)))
            data["images"] = imgs

            responses.append(ProductResponse(**data))
        return responses

product_service = ProductService()
