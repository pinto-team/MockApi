from pydantic import BaseModel
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from app.config import get_settings
from app.models.file import File, FileCreate, FileUpdate
from uuid import UUID, uuid4
from datetime import datetime

settings = get_settings()
client = AsyncIOMotorClient(settings.mongo_url)
db = client[settings.mongo_db]

class MongoCRUD:
    def __init__(self, collection: str, model_cls: BaseModel, create_cls: BaseModel, update_cls: BaseModel):
        self.collection = db[collection]
        self.model_cls = model_cls
        self.create_cls = create_cls
        self.update_cls = update_cls

    async def create(self, data: BaseModel):
        data_dict = data.dict(exclude_unset=True)
        # اضافه کردن id و created_at اگر وجود نداشته باشند
        data_dict["id"] = str(uuid4())  # تولید UUID به جای استفاده از ObjectId
        data_dict["created_at"] = data_dict.get("created_at", datetime.utcnow())
        result = await self.collection.insert_one(data_dict)
        return self.model_cls(**data_dict)

class FileService(MongoCRUD):
    def __init__(self):
        super().__init__(
            collection="files",
            model_cls=File,
            create_cls=FileCreate,
            update_cls=FileUpdate
        )

file_service = FileService()