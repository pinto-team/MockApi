from app.models.brand import Brand, BrandCreate, BrandUpdate
from .base import MongoCRUD


class BrandService(MongoCRUD):
    def __init__(self):
        super().__init__(
            collection="brands",
            model_cls=Brand,
            create_cls=BrandCreate,
            update_cls=BrandUpdate
        )

    # فعلاً وابستگی خاصی نداره، ولی اینجا می‌تونیم در آینده لاجیک اضافه کنیم


brand_service = BrandService()
