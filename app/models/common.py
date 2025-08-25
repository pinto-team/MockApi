from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID, uuid4

class Timestamps(BaseModel):
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class IDModel(BaseModel):
    id: UUID = Field(default_factory=uuid4)

class PaginationMeta(BaseModel):
    page: int
    limit: int
    total: int

class ListResponse(BaseModel):
    items: list
    pagination: PaginationMeta
