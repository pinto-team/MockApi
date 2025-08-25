from fastapi import APIRouter, HTTPException, Query
from uuid import UUID
from typing import List, Optional

from app.models.warehouse import Warehouse, WarehouseCreate, WarehouseUpdate
from app.services.warehouse_service import warehouse_service

router = APIRouter()

@router.get('/', response_model=List[Warehouse])
async def list_warehouses(
    search: Optional[str] = Query(None, description="Search warehouses by name or location"),
    sort_by: Optional[str] = Query(None, description="Sort by 'name' or 'created_at' (asc/desc)")
):
    warehouses = await warehouse_service.list()

    # فیلتر با search
    if search:
        warehouses = [
            w for w in warehouses
            if search.lower() in w.name.lower() or (w.location and search.lower() in w.location.lower())
        ]

    # مرتب‌سازی
    if sort_by:
        if sort_by == "name":
            warehouses = sorted(warehouses, key=lambda w: w.name)
        elif sort_by == "name_desc":
            warehouses = sorted(warehouses, key=lambda w: w.name, reverse=True)
        elif sort_by == "created_at":
            warehouses = sorted(warehouses, key=lambda w: w.created_at)
        elif sort_by == "created_at_desc":
            warehouses = sorted(warehouses, key=lambda w: w.created_at, reverse=True)

    return warehouses

@router.get('/{warehouse_id}', response_model=Warehouse)
async def get_warehouse(warehouse_id: UUID):
    warehouse = await warehouse_service.get(warehouse_id)
    if not warehouse:
        raise HTTPException(404, 'Warehouse not found')
    return warehouse

@router.post('/', response_model=Warehouse)
async def create_warehouse(payload: WarehouseCreate):
    return await warehouse_service.create(payload)

@router.put('/{warehouse_id}', response_model=Warehouse)
async def update_warehouse(warehouse_id: UUID, payload: WarehouseUpdate):
    warehouse = await warehouse_service.update(warehouse_id, payload)
    if not warehouse:
        raise HTTPException(404, 'Warehouse not found')
    return warehouse

@router.delete('/{warehouse_id}')
async def delete_warehouse(warehouse_id: UUID):
    success = await warehouse_service.delete(warehouse_id)
    if not success:
        raise HTTPException(404, 'Warehouse not found')
    return {'status': 'deleted'}
