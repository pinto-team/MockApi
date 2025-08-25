from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.routes.product_routes import router as products_router
from app.routes.store_routes import router as stores_router
from app.routes.category_routes import router as categories_router
from app.routes.brand_routes import router as brands_router
from app.routes.warehouse_routes import router as warehouses_router
from app.routes.image_routes import router as images_router

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # اینجا می‌تونی eventهای استارت یا کلوز دیتابیس رو بذاری
    yield

app = FastAPI(
    title=settings.project_name,
    description="🛒 Mock API server for frontend testing until backend is ready",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",       # Swagger UI
    redoc_url="/redoc",     # Redoc UI
    openapi_url="/openapi.json"
)

# ✅ CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # همه Origin ها مجاز (میتونی محدود کنی)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Routers
app.include_router(products_router, prefix="/products", tags=["Products"])
app.include_router(stores_router, prefix="/stores", tags=["Stores"])
app.include_router(categories_router, prefix="/categories", tags=["Categories"])
app.include_router(brands_router, prefix="/brands", tags=["Brands"])
app.include_router(warehouses_router, prefix="/warehouses", tags=["Warehouses"])
app.include_router(images_router, prefix="/images", tags=["Images"])

@app.get("/health", tags=["Health"])
async def health():
    return {"status": "ok"}
