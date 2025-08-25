from app.services.base import InMemoryCRUD
from app.models.user import User, UserCreate, UserUpdate

user_service = InMemoryCRUD(
    model_cls=User,
    create_cls=UserCreate,
    update_cls=UserUpdate,
    search_fields=["name","email"],
    unique_fields=["email"],
    sortable_fields=["name","created_at","updated_at"],
)
