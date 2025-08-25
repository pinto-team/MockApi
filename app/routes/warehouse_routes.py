from fastapi import APIRouter, HTTPException
from uuid import UUID
from typing import List

from app.models.warehouse import Warehouse, WarehouseCreate, WarehouseUpdate
from app.services.warehouse_service import warehouse_service

router = APIRouter()

@router.get('/', response_model=List[Warehouse])
async def list_warehouses():
    return await warehouse_service.list()

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
