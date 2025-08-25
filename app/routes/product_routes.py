from typing import Optional
from fastapi import APIRouter, HTTPException, Query
from app.routes.router_factory import build_crud_router
from app.services.product_service import product_service
from app.services.faker_utils import fake_product_create
from app.models.product import Product, ProductCreate, ProductUpdate

# Seed via Faker
def _seed(n: int) -> int:
    added = 0
    for _ in range(n):
        product_service.create(fake_product_create())
        added += 1
    return added

router: APIRouter = build_crud_router(
    resource_name="product",
    service=product_service,
    CreateModel=ProductCreate,
    UpdateModel=ProductUpdate,
    Model=Product,
    allowed_filters=["brand", "category_id", "seller_id", "warehouse_id", "is_active"],
    seed_fn=_seed,
)

# --------- Extra endpoint: price quote ---------
@router.get("/{item_id}/price-quote")
def price_quote(item_id: str, qty: int = Query(..., ge=1)):
    """
    Return the effective unit price for the given quantity,
    using pricing_tiers if available; otherwise base_price.
    """
    from uuid import UUID
    obj = product_service.get(item_id) or product_service.get(UUID(item_id))
    if not obj:
        raise HTTPException(status_code=404, detail="product not found")

    unit_price = obj.base_price
    if obj.pricing_tiers:
        # choose the best tier where min_qty <= qty and price is minimal
        applicable = [t for t in obj.pricing_tiers if t.min_qty <= qty]
        if applicable:
            unit_price = min(t.unit_price for t in applicable)

    return {
        "product_id": str(obj.id),
        "qty": qty,
        "unit_price": unit_price,
        "currency": obj.currency,
        "base_price": obj.base_price,
    }
