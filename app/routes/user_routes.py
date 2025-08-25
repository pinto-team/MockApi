from fastapi import APIRouter
from app.routes.router_factory import build_crud_router
from app.services.user_service import user_service
from app.services.faker_utils import fake_user_create
from app.models.user import User, UserCreate, UserUpdate

# Simple seed function using faker
from typing import Any

def _seed(n: int) -> int:
    added = 0
    for _ in range(n):
        user_service.create(fake_user_create())
        added += 1
    return added

router: APIRouter = build_crud_router(
    resource_name="user",
    service=user_service,
    CreateModel=UserCreate,
    UpdateModel=UserUpdate,
    Model=User,
    allowed_filters=["role","is_active"],
    seed_fn=_seed,
)
