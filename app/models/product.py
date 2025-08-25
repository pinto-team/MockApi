from __future__ import annotations
from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from datetime import datetime
from typing import Dict, List, Optional

from .warehouse import WarehouseStock, Warehouse
from .store import Store
from .category import Category
from .brand import Brand
from .image import Image

class ProductBase(BaseModel):
    sku: str
    name: str
    price: float
    attributes: Dict[str, str] | None = None
    stock: int
    store_id: UUID
    category_id: UUID
    brand_id: UUID
    warehouse_availability: List[WarehouseStock] | None = None

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    sku: str | None = None
    name: str | None = None
    price: float | None = None
    attributes: Dict[str, str] | None = None
    stock: int | None = None
    store_id: UUID | None = None
    category_id: UUID | None = None
    brand_id: UUID | None = None
    warehouse_availability: List[WarehouseStock] | None = None

class Product(ProductBase):
    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class WarehouseAvailabilityResponse(WarehouseStock):
    warehouse: Warehouse | None = None

class ProductResponse(Product):
    store: Store | None = None
    category: Category | None = None
    brand: Brand | None = None
    images: List[Image] | None = None
    warehouse_availability: List[WarehouseAvailabilityResponse] | None = None
