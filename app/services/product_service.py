from uuid import UUID
from typing import List, Optional
from pymongo import ASCENDING, DESCENDING

from . import file_service
from .base import MongoCRUD, _serialize
from app.models.product import (
    Product,
    ProductCreate,
    ProductUpdate,
    ProductResponse,
    WarehouseAvailabilityResponse
)
from app.models.store import Store
from app.models.category import Category
from app.models.brand import Brand
from app.models.warehouse import Warehouse
from app.db.mongo import db
from app.services.category_service import category_service
from app.services.brand_service import brand_service


class ProductService(MongoCRUD):
    def __init__(self):
        super().__init__(
            collection="products",
            model_cls=Product,
            create_cls=ProductCreate,
            update_cls=ProductUpdate
        )

    async def create(self, payload: ProductCreate) -> Product:
        """اینجا قبل از ساخت محصول، بررسی می‌کنیم که برند و دسته‌بندی واقعاً وجود داشته باشند"""
        # ✅ بررسی برند
        brand = await brand_service.get(payload.brand_id)
        if not brand:
            raise ValueError(f"Brand with id {payload.brand_id} does not exist")

        # ✅ بررسی دسته‌بندی
        category = await category_service.get(payload.category_id)
        if not category:
            raise ValueError(f"Category with id {payload.category_id} does not exist")

        # ذخیره محصول
        return await super().create(payload)

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

        # ✅ استفاده مستقیم از self.collection
        cursor = self.collection.find(query)

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
            if getattr(p, "images", []):
                for fid in p.images:
                    f_doc = await file_service.get(fid)
                    if f_doc:
                        imgs.append(f_doc)
            data["images"] = imgs

            responses.append(ProductResponse(**data))
        return responses


product_service = ProductService()
