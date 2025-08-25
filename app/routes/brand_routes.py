from fastapi import APIRouter, HTTPException, Query
from uuid import UUID
from typing import List, Optional

from app.models.brand import Brand, BrandCreate, BrandUpdate
from app.services.brand_service import brand_service

router = APIRouter()

@router.get('/', response_model=List[Brand])
async def list_brands(
    name: Optional[str] = Query(None, description="Filter by brand name"),
    country: Optional[str] = Query(None, description="Filter by brand country")
):
    brands = await brand_service.list()
    if name:
        brands = [b for b in brands if name.lower() in b.name.lower()]
    if country:
        brands = [b for b in brands if b.country and country.lower() in b.country.lower()]
    return brands

@router.get('/{brand_id}', response_model=Brand)
async def get_brand(brand_id: UUID):
    brand = await brand_service.get(brand_id)
    if not brand:
        raise HTTPException(404, 'Brand not found')
    return brand

@router.post('/', response_model=Brand)
async def create_brand(payload: BrandCreate):
    return await brand_service.create(payload)

@router.put('/{brand_id}', response_model=Brand)
async def update_brand(brand_id: UUID, payload: BrandUpdate):
    brand = await brand_service.update(brand_id, payload)
    if not brand:
        raise HTTPException(404, 'Brand not found')
    return brand

@router.delete('/{brand_id}')
async def delete_brand(brand_id: UUID):
    success = await brand_service.delete(brand_id)
    if not success:
        raise HTTPException(404, 'Brand not found')
    return {'status': 'deleted'}
