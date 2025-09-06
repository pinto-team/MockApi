from fastapi import APIRouter, HTTPException, Query, Request
from uuid import UUID
from typing import Optional, List

from app.models.warehouse import Warehouse, WarehouseCreate, WarehouseUpdate
from app.models.response import ApiSuccessResponse, SuccessMeta, PaginationMeta
from app.services.warehouse_service import warehouse_service

router = APIRouter()

@router.get("", response_model=ApiSuccessResponse[List[Warehouse]])
async def list_warehouses(
    request: Request,
    name: Optional[str] = Query(None, description="Filter by warehouse name"),
    location: Optional[str] = Query(None, description="Filter by location"),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
):
    filters = {}
    if name:
        filters["name"] = name
    if location:
        filters["location"] = location

    items, total = await warehouse_service.list(filters, page, limit)

    pagination = PaginationMeta(page=page, limit=limit, total=total)
    meta = SuccessMeta(
        message="warehouses.list.success",
        method=request.method,
        path=request.url.path,
        host=request.client.host if request.client else None,
        pagination=pagination,
    )
    return ApiSuccessResponse(data=items, meta=meta)

@router.post("", response_model=ApiSuccessResponse[Warehouse], status_code=201)
async def create_warehouse(request: Request, payload: WarehouseCreate):
    created = await warehouse_service.create(payload)
    meta = SuccessMeta(
        message="warehouses.create.success",
        method=request.method,
        path=request.url.path,
        host=request.client.host if request.client else None,
    )
    return ApiSuccessResponse(data=created, meta=meta)

@router.get("/{warehouse_id}", response_model=ApiSuccessResponse[Warehouse])
async def get_warehouse(request: Request, warehouse_id: UUID):
    warehouse = await warehouse_service.get(warehouse_id)
    if not warehouse:
        raise HTTPException(status_code=404, detail="Warehouse not found")
    meta = SuccessMeta(
        message="warehouses.get.success",
        method=request.method,
        path=request.url.path,
        host=request.client.host if request.client else None,
    )
    return ApiSuccessResponse(data=warehouse, meta=meta)

@router.put("/{warehouse_id}", response_model=ApiSuccessResponse[Warehouse])
async def update_warehouse(request: Request, warehouse_id: UUID, payload: WarehouseUpdate):
    updated = await warehouse_service.update(warehouse_id, payload)
    if not updated:
        raise HTTPException(status_code=404, detail="Warehouse not found")
    meta = SuccessMeta(
        message="warehouses.update.success",
        method=request.method,
        path=request.url.path,
        host=request.client.host if request.client else None,
    )
    return ApiSuccessResponse(data=updated, meta=meta)

@router.delete("/{warehouse_id}", response_model=ApiSuccessResponse[dict])
async def delete_warehouse(request: Request, warehouse_id: UUID):
    ok = await warehouse_service.delete(warehouse_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Warehouse not found")
    meta = SuccessMeta(
        message="warehouses.delete.success",
        method=request.method,
        path=request.url.path,
        host=request.client.host if request.client else None,
    )
    return ApiSuccessResponse(data={"status": "deleted"}, meta=meta)
