from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from datetime import datetime

class BrandBase(BaseModel):
    name: str
    description: str | None = None
    country: str | None = None
    website: str | None = None
    logo_url: str | None = None

class BrandCreate(BrandBase):
    pass

class BrandUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    country: str | None = None
    website: str | None = None
    logo_url: str | None = None

class Brand(BrandBase):
    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
