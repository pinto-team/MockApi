from pydantic import BaseModel, Field, AnyUrl
from uuid import UUID, uuid4
from datetime import datetime

class ImageBase(BaseModel):
    product_id: UUID
    url: AnyUrl

class ImageCreate(ImageBase):
    pass

class ImageUpdate(BaseModel):
    url: AnyUrl | None = None

class Image(ImageBase):
    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
