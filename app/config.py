from functools import lru_cache
from pydantic import BaseModel
import os

class Settings(BaseModel):
    project_name: str = "Wholesale Supermarket API"
    debug: bool = True

    # you can extend with DB_URL, etc.
    # DB_URL: str = os.getenv("DB_URL", "sqlite://:memory:")

@lru_cache
def get_settings() -> Settings:
    return Settings()
