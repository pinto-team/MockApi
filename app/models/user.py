from typing import Optional
from pydantic import BaseModel, Field, EmailStr, constr
from uuid import UUID, uuid4
from datetime import datetime

RoleStr = constr(pattern=r"^(buyer|seller|admin)$")

class UserBase(BaseModel):
    name: constr(min_length=1, max_length=120)
    email: EmailStr
    role: RoleStr = "buyer"
    is_active: bool = True

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    name: Optional[constr(min_length=1, max_length=120)] = None
    email: Optional[EmailStr] = None
    role: Optional[RoleStr] = None
    is_active: Optional[bool] = None

class User(UserBase):
    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
