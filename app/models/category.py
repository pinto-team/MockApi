from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from datetime import datetime

class CategoryBase(BaseModel):
    name: str
    description: str | None = None
    parent_id: UUID | None = None
    image_url: str | None = None

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    parent_id: UUID | None = None
    image_url: str | None = None

class Category(CategoryBase):
    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
