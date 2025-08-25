from app.models.brand import Brand, BrandCreate, BrandUpdate
from .base import MongoCRUD

brand_service = MongoCRUD(
    collection="brands",
    model_cls=Brand,
    create_cls=BrandCreate,
    update_cls=BrandUpdate
)
