from functools import lru_cache
from pydantic import BaseModel
import os

class Settings(BaseModel):
    project_name: str = "Wholesale Supermarket API"
    debug: bool = True

    # auto seed
    auto_seed_enabled: bool = (os.getenv("AUTO_SEED_ENABLED", "true").lower() == "true")
    auto_seed_count_products: int = int(os.getenv("AUTO_SEED_COUNT_PRODUCTS", "100"))
    auto_seed_count_users: int = int(os.getenv("AUTO_SEED_COUNT_USERS", "50"))
    # optional deterministic seed
    faker_seed: int | None = int(os.getenv("FAKER_SEED")) if os.getenv("FAKER_SEED") else None

@lru_cache
def get_settings() -> Settings:
    return Settings()
