from __future__ import annotations
from pydantic import BaseModel, Field, AnyUrl
from uuid import UUID, uuid4
from datetime import datetime
from typing import Dict, List, Optional
from app.models.file import File

from .warehouse import WarehouseStock, Warehouse
from .store import Store
from .category import Category
from .brand import Brand

class PricingTier(BaseModel):
    min_qty: int
    unit_price: float
    currency: str | None = None

class Dimensions(BaseModel):
    length: float
    width: float
    height: float
    unit: str = "cm"

class NutritionFacts(BaseModel):
    calories: float | None = None
    fat: float | None = None
    protein: float | None = None
    carbohydrates: float | None = None

class ProductBase(BaseModel):
    sku: str
    name: str
    full_name: str | None = None
    description: str | None = None
    brand_id: str | None = None
    category_id: str | None = None

    price: float
    wholesale_price: float | None = None
    purchase_price: float | None = None
    currency: str = "USD"
    tax_rate: float | None = None
    pricing_tiers: List[PricingTier] | None = None

    unit_of_sale: str | None = None
    pack_size: int | None = None
    case_size: int | None = None
    pallet_size: int | None = None

    barcode: str | None = None
    barcode_type: str | None = None

    attributes: Dict[str, str] | None = None       # آزاد (Key/Value)
    weight: float | None = None
    weight_unit: str | None = "kg"
    dimensions: Dimensions | None = None
    packaging: str | None = None
    storage: str | None = None
    shelf_life_days: int | None = None
    halal: bool | None = None

    allow_backorder: bool = False
    is_active: bool = True
    tags: List[str] | None = None
    certifications: List[str] | None = None

    ingredients: List[str] | None = None
    nutrition_facts: NutritionFacts | None = None
    warranty_months: int | None = None
    returnable: bool | None = None

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    sku: str | None = None
    name: str | None = None
    full_name: str | None = None
    description: str | None = None
    brand_id: UUID | None = None
    category_id: UUID | None = None
    price: float | None = None
    wholesale_price: float | None = None
    purchase_price: float | None = None
    currency: str | None = None
    tax_rate: float | None = None
    pricing_tiers: List[PricingTier] | None = None
    unit_of_sale: str | None = None
    pack_size: int | None = None
    case_size: int | None = None
    pallet_size: int | None = None
    barcode: str | None = None
    barcode_type: str | None = None
    attributes: Dict[str, str] | None = None
    weight: float | None = None
    weight_unit: str | None = None
    dimensions: Dimensions | None = None
    packaging: str | None = None
    storage: str | None = None
    shelf_life_days: int | None = None
    halal: bool | None = None
    allow_backorder: bool | None = None
    is_active: bool | None = None
    tags: List[str] | None = None
    certifications: List[str] | None = None
    ingredients: List[str] | None = None
    nutrition_facts: NutritionFacts | None = None
    warranty_months: int | None = None
    returnable: bool | None = None

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
    images: List[File] | None = None  # populate می‌شه
    warehouse_availability: List[WarehouseAvailabilityResponse] | None = None