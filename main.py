from fastapi import FastAPI
from app.config import get_settings
from app.routes.product_routes import router as products_router
from app.routes.user_routes import router as users_router

settings = get_settings()
app = FastAPI(title=settings.project_name)

app.include_router(products_router, prefix="/products", tags=["Products"])
app.include_router(users_router, prefix="/users", tags=["Users"])

@app.get("/health")
def health():
    return {"status": "ok"}
