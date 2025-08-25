from app.services.base import InMemoryCRUD
from app.models.product import Product, ProductCreate, ProductUpdate

product_service = InMemoryCRUD(
    model_cls=Product,
    create_cls=ProductCreate,
    update_cls=ProductUpdate,
    search_fields=["name","sku"],
    unique_fields=["sku"],
    sortable_fields=["name","base_price","stock","created_at","updated_at"],
)
