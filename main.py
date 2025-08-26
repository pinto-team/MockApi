from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import get_settings
from app.routes.product_routes import router as products_router
from app.routes.store_routes import router as stores_router
from app.routes.category_routes import router as categories_router
from app.routes.brand_routes import router as brands_router
from app.routes.warehouse_routes import router as warehouses_router
from app.routes.user_routes import router as users_router
from app.routes.upload_routes import router as upload_router

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
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
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ✅ Routers
app.mount("/static", StaticFiles(directory="uploads"), name="static")
app.include_router(users_router, prefix="/users", tags=["Users"])
app.include_router(upload_router, prefix="/files", tags=["Upload"])
app.include_router(products_router, prefix="/products", tags=["Products"])
app.include_router(stores_router, prefix="/stores", tags=["Stores"])
app.include_router(categories_router, prefix="/categories", tags=["Categories"])
app.include_router(brands_router, prefix="/brands", tags=["Brands"])
app.include_router(warehouses_router, prefix="/warehouses", tags=["Warehouses"])

@app.get("/health", tags=["Health"])
async def health():
    return {"status": "ok"}
