#!/usr/bin/env python3
"""
Quickly scaffold a new resource.
Usage:
  python scripts/new_resource.py Warehouse
This will create:
  - app/models/warehouse.py
  - app/services/warehouse_service.py
  - app/routes/warehouse_routes.py
Then you must include the router in app/main.py
"""
import os, sys, textwrap

TEMPLATE_MODEL = """from typing import Optional
from pydantic import BaseModel, Field, constr
from uuid import UUID, uuid4
from datetime import datetime

class {Name}Base(BaseModel):
    name: constr(min_length=1, max_length=120)
    is_active: bool = True

class {Name}Create({Name}Base):
    pass

class {Name}Update(BaseModel):
    name: Optional[constr(min_length=1, max_length=120)] = None
    is_active: Optional[bool] = None

class {Name}({Name}Base):
    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
"""

TEMPLATE_SERVICE = """from app.services.base import InMemoryCRUD
from app.models.{name} import {Name}, {Name}Create, {Name}Update

{name}_service = InMemoryCRUD(
    model_cls={Name},
    create_cls={Name}Create,
    update_cls={Name}Update,
    search_fields=[\"name\"],
    unique_fields=[],  # add unique fields if needed
    sortable_fields=[\"name\",\"created_at\",\"updated_at\"],
)
"""

TEMPLATE_ROUTE = """from fastapi import APIRouter
from app.routes.router_factory import build_crud_router
from app.services.{name}_service import {name}_service
from app.models.{name} import {Name}, {Name}Create, {Name}Update

def _seed(n: int) -> int:
    # Optional: implement a faker-based seeder for this resource
    return 0

router: APIRouter = build_crud_router(
    resource_name="{name}",
    service={name}_service,
    CreateModel={Name}Create,
    UpdateModel={Name}Update,
    Model={Name},
    allowed_filters=[\"is_active\"],
    seed_fn=_seed,
)
"""

def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/new_resource.py <ResourceName>")
        sys.exit(1)
    Name = sys.argv[1]
    name = Name[0].lower() + Name[1:]
    base = os.path.dirname(os.path.dirname(__file__))
    write(os.path.join(base, "app", "models", f"{name}.py"), TEMPLATE_MODEL.format(Name=Name))
    write(os.path.join(base, "app", "services", f"{name}_service.py"), TEMPLATE_SERVICE.format(Name=Name, name=name))
    write(os.path.join(base, "app", "routes", f"{name}_routes.py"), TEMPLATE_ROUTE.format(Name=Name, name=name))
    print(f"Scaffolded model/service/route for {Name}. Now include the router in app/main.py")

if __name__ == "__main__":
    main()
