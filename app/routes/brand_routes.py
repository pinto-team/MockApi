from fastapi import APIRouter, HTTPException, Query, Request
from uuid import UUID
from typing import Optional, List

from app.models.brand import Brand, BrandCreate, BrandUpdate
from app.models.response import ApiSuccessResponse, SuccessMeta, PaginationMeta
from app.services.brand_service import brand_service
from app.services.file_service import file_service

router = APIRouter()


@router.get("", response_model=ApiSuccessResponse[List[Brand]])
async def list_brands(
    request: Request,
    name: Optional[str] = Query(None, description="Filter by brand name"),
    country: Optional[str] = Query(None, description="Filter by brand country"),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
):
    filters = {}
    if name:
        filters["name"] = name
    if country:
        filters["country"] = country

    items, total = await brand_service.list(filters, page, limit)

    pagination = PaginationMeta(page=page, limit=limit, total=total)
    meta = SuccessMeta(
        message="brands.list.success",
        method=request.method,
        path=request.url.path,
        host=request.client.host if request.client else None,
        pagination=pagination,  # PaginationMeta داخل SuccessMeta
    )
    return ApiSuccessResponse(data=items, meta=meta)


async def _ensure_logo_url_from_id(payload_dict: dict) -> dict:
    """
    - اگر logo_id مقدار دارد → url فایل را روی logo_url ست کن.
    - اگر logo_id صراحتاً None است → logo_url را هم None کن (پاک‌سازی لوگو).
    - در غیر این‌صورت هیچ تغییری نده.
    """
    if "logo_id" in payload_dict:
        logo_id = payload_dict.get("logo_id")
        if logo_id:
            file_obj = await file_service.get(logo_id)
            if not file_obj:
                raise HTTPException(status_code=400, detail="لوگو با این شناسه پیدا نشد")
            payload_dict["logo_url"] = file_obj.url
        else:
            payload_dict["logo_url"] = None
    return payload_dict


@router.post("", response_model=ApiSuccessResponse[Brand], status_code=201)
async def create_brand(request: Request, payload: BrandCreate):
    data = payload.dict(exclude_unset=True)
    # logo_url از کلاینت پذیرفته نمی‌شود؛ سرور خودش ست می‌کند
    data.pop("logo_url", None)
    data = await _ensure_logo_url_from_id(data)

    created = await brand_service.create(BrandCreate(**data))
    meta = SuccessMeta(
        message="brands.create.success",
        method=request.method,
        path=request.url.path,
        host=request.client.host if request.client else None,
    )
    return ApiSuccessResponse(data=created, meta=meta)


@router.get("/{brand_id}", response_model=ApiSuccessResponse[Brand])
async def get_brand(request: Request, brand_id: UUID):
    brand = await brand_service.get(brand_id)
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")

    meta = SuccessMeta(
        message="brands.get.success",
        method=request.method,
        path=request.url.path,
        host=request.client.host if request.client else None,
    )
    return ApiSuccessResponse(data=brand, meta=meta)


@router.put("/{brand_id}", response_model=ApiSuccessResponse[Brand])
async def update_brand(request: Request, brand_id: UUID, payload: BrandUpdate):
    data = payload.dict(exclude_unset=True)
    data.pop("logo_url", None)  # از کلاینت قبول نمی‌کنیم
    data = await _ensure_logo_url_from_id(data)

    updated = await brand_service.update(brand_id, BrandUpdate(**data))
    if not updated:
        raise HTTPException(status_code=404, detail="Brand not found")

    meta = SuccessMeta(
        message="brands.update.success",
        method=request.method,
        path=request.url.path,
        host=request.client.host if request.client else None,
    )
    return ApiSuccessResponse(data=updated, meta=meta)


@router.delete("/{brand_id}", response_model=ApiSuccessResponse[dict])
async def delete_brand(request: Request, brand_id: UUID):
    ok = await brand_service.delete(brand_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Brand not found")

    meta = SuccessMeta(
        message="brands.delete.success",
        method=request.method,
        path=request.url.path,
        host=request.client.host if request.client else None,
    )
    return ApiSuccessResponse(data={"status": "deleted"}, meta=meta)
