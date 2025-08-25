from typing import Optional, List
from pydantic import BaseModel, Field, constr, conint, confloat, field_validator, model_validator, AnyUrl
from uuid import UUID, uuid4
from datetime import datetime

SkuStr = constr(pattern=r"^[A-Z0-9-]+$", strip_whitespace=True)
CurrencyStr = constr(pattern=r"^[A-Z]{3}$", strip_whitespace=True)
BarcodeStr = constr(pattern=r"^[0-9]{8,14}$", strip_whitespace=True)

class PricingTier(BaseModel):
    min_qty: conint(ge=1)
    unit_price: confloat(ge=0)

class WarehouseAvailability(BaseModel):
    warehouse_id: UUID
    stock: conint(ge=0)
    lead_time_days: conint(ge=0) = 0

class Dimensions(BaseModel):
    length: confloat(ge=0)
    width: confloat(ge=0)
    height: confloat(ge=0)

class Attributes(BaseModel):
    weight: Optional[confloat(ge=0)] = None
    dimensions: Optional[Dimensions] = None
    packaging: Optional[str] = None
    storage: Optional[str] = None
    shelf_life_days: Optional[conint(ge=0)] = None
    halal: Optional[bool] = None

class ProductBase(BaseModel):
    seller_id: UUID
    warehouse_id: UUID
    sku: SkuStr
    name: constr(min_length=1, max_length=255)
    description: Optional[str] = None
    category_id: UUID
    brand: Optional[constr(max_length=100)] = None
    base_price: confloat(ge=0)
    purchase_price: Optional[confloat(ge=0)] = None
    currency: CurrencyStr = "USD"
    tax_rate: confloat(ge=0) = 0
    min_order_quantity: conint(ge=1) = 1
    min_order_multiple: Optional[conint(ge=1)] = None
    stock: conint(ge=0) = 0
    warehouse_availability: Optional[List[WarehouseAvailability]] = None
    pricing_tiers: Optional[List[PricingTier]] = None
    uom: Optional[str] = None
    pack_size: Optional[conint(ge=1)] = None
    case_size: Optional[conint(ge=1)] = None
    barcode: Optional[BarcodeStr] = None
    attributes: Optional[Attributes] = None
    allow_backorder: bool = False
    is_active: bool = True
    images: Optional[List[AnyUrl]] = None
    tags: Optional[List[str]] = None

    # ---------- Field-level validators ----------

    @field_validator("sku")
    @classmethod
    def sku_upper(cls, v: str) -> str:
        return v.upper()

    @field_validator("currency")
    @classmethod
    def currency_upper(cls, v: str) -> str:
        return v.upper()

    @field_validator("images")
    @classmethod
    def images_rules(cls, v: Optional[List[AnyUrl]]) -> Optional[List[AnyUrl]]:
        # allow None or 1..4 items
        if v is None:
            return v
        if not (1 <= len(v) <= 4):
            raise ValueError("images must contain between 1 and 4 URLs")
        return v

    # ---------- Model-level validators ----------

    @model_validator(mode="after")
    def check_business_rules(self):
        # purchase_price should not exceed base_price
        if self.purchase_price is not None and self.purchase_price > self.base_price:
            raise ValueError("purchase_price cannot be greater than base_price")

        # pricing tiers sorted by min_qty + unit_price <= base_price
        if self.pricing_tiers:
            prev = 0
            for tier in sorted(self.pricing_tiers, key=lambda t: t.min_qty):
                if tier.min_qty <= prev:
                    raise ValueError("pricing_tiers must be strictly increasing by min_qty")
                prev = tier.min_qty
                if tier.unit_price > self.base_price:
                    raise ValueError("tier unit_price cannot exceed base_price")

        # If min_order_multiple is set, it must be >= 1 (already) and also should not exceed min_order_quantity (optional rule)
        if self.min_order_multiple is not None and self.min_order_multiple < 1:
            raise ValueError("min_order_multiple must be >= 1")

        return self

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    seller_id: Optional[UUID] = None
    warehouse_id: Optional[UUID] = None
    sku: Optional[SkuStr] = None
    name: Optional[constr(min_length=1, max_length=255)] = None
    description: Optional[str] = None
    category_id: Optional[UUID] = None
    brand: Optional[constr(max_length=100)] = None
    base_price: Optional[confloat(ge=0)] = None
    purchase_price: Optional[confloat(ge=0)] = None
    currency: Optional[CurrencyStr] = None
    tax_rate: Optional[confloat(ge=0)] = None
    min_order_quantity: Optional[conint(ge=1)] = None
    min_order_multiple: Optional[conint(ge=1)] = None
    stock: Optional[conint(ge=0)] = None
    warehouse_availability: Optional[List[WarehouseAvailability]] = None
    pricing_tiers: Optional[List[PricingTier]] = None
    uom: Optional[str] = None
    pack_size: Optional[conint(ge=1)] = None
    case_size: Optional[conint(ge=1)] = None
    barcode: Optional[BarcodeStr] = None
    attributes: Optional[Attributes] = None
    allow_backorder: Optional[bool] = None
    is_active: Optional[bool] = None
    images: Optional[List[AnyUrl]] = None
    tags: Optional[List[str]] = None

class Product(ProductBase):
    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
