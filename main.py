from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.config import get_settings
from app.routes.product_routes import router as products_router
from app.routes.store_routes import router as stores_router
from app.routes.category_routes import router as categories_router
from app.routes.brand_routes import router as brands_router
from app.routes.warehouse_routes import router as warehouses_router
from app.routes.image_routes import router as images_router
from app.services.seed import seed_data

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await seed_data()
    yield

app = FastAPI(title=settings.project_name, lifespan=lifespan)

app.include_router(products_router, prefix="/products", tags=["Products"])
app.include_router(stores_router, prefix="/stores", tags=["Stores"])
app.include_router(categories_router, prefix="/categories", tags=["Categories"])
app.include_router(brands_router, prefix="/brands", tags=["Brands"])
app.include_router(warehouses_router, prefix="/warehouses", tags=["Warehouses"])
app.include_router(images_router, prefix="/images", tags=["Images"])

@app.get("/health")
async def health():
    return {"status": "ok"}
