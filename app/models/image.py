from pydantic import BaseModel, Field, AnyUrl
from uuid import UUID, uuid4
from datetime import datetime

class ImageBase(BaseModel):
    product_id: UUID | None = None   # می‌تونه به محصول یا برند یا دسته‌بندی وصل باشه
    url: AnyUrl
    alt_text: str | None = None      # متن جایگزین برای SEO و دسترس‌پذیری
    is_primary: bool = False         # عکس اصلی محصول یا خیر
    sort_order: int | None = None    # ترتیب نمایش

class ImageCreate(ImageBase):
    pass

class ImageUpdate(BaseModel):
    url: AnyUrl | None = None
    alt_text: str | None = None
    is_primary: bool | None = None
    sort_order: int | None = None

class Image(ImageBase):
    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
