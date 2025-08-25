from fastapi import APIRouter
from app.routes.router_factory import build_crud_router
from app.services.product_service import product_service
from app.services.faker_utils import fake_product_create
from app.models.product import Product, ProductCreate, ProductUpdate

# Simple seed function using faker
from typing import Any

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
    allowed_filters=["brand","category_id","seller_id","warehouse_id","is_active"],
    seed_fn=_seed,
)
