from app.models.image import Image, ImageCreate, ImageUpdate
from .base import MongoCRUD

image_service = MongoCRUD(collection="images", model_cls=Image, create_cls=ImageCreate, update_cls=ImageUpdate)
