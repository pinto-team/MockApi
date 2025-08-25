from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.config import get_settings
from app.routes.product_routes import router as products_router
from app.routes.user_routes import router as users_router

# services + faker utils
from app.services.product_service import product_service
from app.services.user_service import user_service
from app.services.faker_utils import fake_product_create, fake_user_create, set_seed

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # ---- startup ----
    if settings.faker_seed is not None:
        set_seed(settings.faker_seed)

    if settings.auto_seed_enabled:
        # اگر خالی است، سید کن
        if not product_service._store:  # in-memory check
            for _ in range(settings.auto_seed_count_products):
                product_service.create(fake_product_create())
        if not user_service._store:
            for _ in range(settings.auto_seed_count_users):
                user_service.create(fake_user_create())
    yield
    # ---- shutdown ----
    # اینجا اگر لازم شد cleanup انجام بدهی (نیازی نیست)

app = FastAPI(title=settings.project_name, lifespan=lifespan)

app.include_router(products_router, prefix="/products", tags=["Products"])
app.include_router(users_router, prefix="/users", tags=["Users"])

@app.get("/health")
def health():
    return {
        "status": "ok",
        "products": len(product_service._store),
        "users": len(user_service._store),
        "auto_seed_enabled": settings.auto_seed_enabled,
    }
