from app.models.category import Category, CategoryCreate, CategoryUpdate
from .base import MongoCRUD

category_service = MongoCRUD(
    collection="categories",
    model_cls=Category,
    create_cls=CategoryCreate,
    update_cls=CategoryUpdate
)
