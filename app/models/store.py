from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from datetime import datetime

class StoreBase(BaseModel):
    name: str

class StoreCreate(StoreBase):
    pass

class StoreUpdate(BaseModel):
    name: str | None = None

class Store(StoreBase):
    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
