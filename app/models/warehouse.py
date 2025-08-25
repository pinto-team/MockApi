from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from datetime import datetime

class WarehouseBase(BaseModel):
    name: str
    location: str | None = None

class WarehouseCreate(WarehouseBase):
    pass

class WarehouseUpdate(BaseModel):
    name: str | None = None
    location: str | None = None

class Warehouse(WarehouseBase):
    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class WarehouseStock(BaseModel):
    warehouse_id: UUID
    stock: int
