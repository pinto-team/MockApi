from fastapi import APIRouter, HTTPException, Query, Request
from uuid import UUID
from typing import Optional, List

from app.models.brand import Brand, BrandCreate, BrandUpdate
from app.models.response import ApiSuccessResponse, SuccessMeta, PaginationMeta
from app.services.brand_service import brand_service

router = APIRouter()


@router.get("", response_model=ApiSuccessResponse[List[Brand]])
async def list_brands(
    request: Request,
    name: Optional[str] = Query(None, description="Filter by brand name"),
    country: Optional[str] = Query(None, description="Filter by brand country"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page"),
):
    brands = await brand_service.list()

    if name:
        brands = [b for b in brands if name.lower() in b.name.lower()]
    if country:
        brands = [b for b in brands if b.country and country.lower() in b.country.lower()]

    total = len(brands)
    start = (page - 1) * limit
    end = start + limit
    items = brands[start:end]

    pagination = PaginationMeta(
        page=page,
        limit=limit,
        total=total,
        total_pages=(total + limit - 1) // limit,
        has_next=end < total,
        has_previous=page > 1,
    )

    meta = SuccessMeta(
        message="brands.list.success",
        method=request.method,
        path=request.url.path,
        query=request.url.query,
        host=request.client.host if request.client else None,
        pagination=pagination,
    )

    return ApiSuccessResponse(data=items, meta=meta)


@router.get("/{brand_id}", response_model=ApiSuccessResponse[Brand])
async def get_brand(request: Request, brand_id: UUID):
    brand = await brand_service.get(brand_id)
    if not brand:
        raise HTTPException(404, "Brand not found")

    meta = SuccessMeta(
        message="brands.get.success",
        method=request.method,
        path=request.url.path,
        host=request.client.host if request.client else None,
    )
    return ApiSuccessResponse(data=brand, meta=meta)


@router.post("", response_model=ApiSuccessResponse[Brand])
async def create_brand(request: Request, payload: BrandCreate):
    brand = await brand_service.create(payload)

    meta = SuccessMeta(
        message="brands.create.success",
        method=request.method,
        path=request.url.path,
        host=request.client.host if request.client else None,
    )
    return ApiSuccessResponse(data=brand, meta=meta)


@router.put("/{brand_id}", response_model=ApiSuccessResponse[Brand])
async def update_brand(request: Request, brand_id: UUID, payload: BrandUpdate):
    brand = await brand_service.update(brand_id, payload)
    if not brand:
        raise HTTPException(404, "Brand not found")

    meta = SuccessMeta(
        message="brands.update.success",
        method=request.method,
        path=request.url.path,
        host=request.client.host if request.client else None,
    )
    return ApiSuccessResponse(data=brand, meta=meta)


@router.delete("/{brand_id}", response_model=ApiSuccessResponse[dict])
async def delete_brand(request: Request, brand_id: UUID):
    success = await brand_service.delete(brand_id)
    if not success:
        raise HTTPException(404, "Brand not found")

    meta = SuccessMeta(
        message="brands.delete.success",
        method=request.method,
        path=request.url.path,
        host=request.client.host if request.client else None,
    )
    return ApiSuccessResponse(data={"status": "deleted"}, meta=meta)
