from motor.motor_asyncio import AsyncIOMotorClient
from app.config import get_settings

settings = get_settings()
client = AsyncIOMotorClient(settings.mongo_url, serverSelectionTimeoutMS=5000)
db = client[settings.mongo_db]

__all__ = ["db"]
