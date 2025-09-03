from fastapi import APIRouter, HTTPException, Query, Request
from uuid import UUID
from typing import List, Optional

from app.models.category import Category, CategoryCreate, CategoryUpdate
from app.services.category_service import category_service
from app.models.response import ApiSuccessResponse, SuccessMeta, PaginationMeta

router = APIRouter()

@router.get("/", response_model=ApiSuccessResponse[List[Category]])
async def list_categories(
    request: Request,
    name: Optional[str] = Query(None, description="Filter by category name"),
    parent_id: Optional[UUID] = Query(None, description="Filter by parent category"),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
):
    filters = {}
    if name:
        filters["name"] = name
    if parent_id:
        filters["parent_id"] = parent_id

    items, total = await category_service.list(filters, page, limit)

    pagination = PaginationMeta(page=page, limit=limit, total=total)
    meta = SuccessMeta(
        message="categories.list.success",
        method=request.method,
        path=request.url.path,
        host=request.client.host if request.client else None,
        pagination=pagination,
    )
    return ApiSuccessResponse(data=items, meta=meta)

@router.get("/{category_id}", response_model=ApiSuccessResponse[Category])
async def get_category(request: Request, category_id: UUID):
    category = await category_service.get(category_id)
    if not category:
        raise HTTPException(404, "Category not found")

    meta = SuccessMeta(
        message="categories.get.success",
        method=request.method,
        path=request.url.path,
        host=request.client.host if request.client else None,
    )
    return ApiSuccessResponse(data=category, meta=meta)

@router.post("/", response_model=ApiSuccessResponse[Category], status_code=201)
async def create_category(request: Request, payload: CategoryCreate):
    created = await category_service.create(payload)
    meta = SuccessMeta(
        message="categories.create.success",
        method=request.method,
        path=request.url.path,
        host=request.client.host if request.client else None,
    )
    return ApiSuccessResponse(data=created, meta=meta)


@router.put("/{category_id}", response_model=ApiSuccessResponse[Category])
async def update_category(request: Request, category_id: UUID, payload: CategoryUpdate):
    category = await category_service.update(category_id, payload)
    if not category:
        raise HTTPException(404, "Category not found")

    meta = SuccessMeta(
        message="categories.update.success",
        method=request.method,
        path=request.url.path,
        host=request.client.host if request.client else None,
    )
    return ApiSuccessResponse(data=category, meta=meta)


@router.delete("/{category_id}", response_model=ApiSuccessResponse[dict])
async def delete_category(request: Request, category_id: UUID):
    success = await category_service.delete(category_id)
    if not success:
        raise HTTPException(404, "Category not found")

    meta = SuccessMeta(
        message="categories.delete.success",
        method=request.method,
        path=request.url.path,
        host=request.client.host if request.client else None,
    )
    return ApiSuccessResponse(data={"status": "deleted"}, meta=meta)
