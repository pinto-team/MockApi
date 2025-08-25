from fastapi import APIRouter, HTTPException, Query
from uuid import UUID
from typing import List, Optional

from app.models.product import ProductResponse, ProductCreate, ProductUpdate
from app.services.product_service import product_service

router = APIRouter()

@router.get('/', response_model=List[ProductResponse])
async def list_products(
    search: Optional[str] = Query(None, description="Search in name, description, tags"),
    sort_by_price: Optional[str] = Query(None, description="Sort by price: 'asc' or 'desc'")
):
    return await product_service.list(search=search, sort_by_price=sort_by_price)

@router.get('/{product_id}', response_model=ProductResponse)
async def get_product(product_id: UUID):
    product = await product_service.get(product_id)
    if not product:
        raise HTTPException(404, 'Product not found')
    return product

@router.post('/', response_model=ProductResponse)
async def create_product(payload: ProductCreate):
    product = await product_service.create(payload)
    return await product_service.get(product.id)

@router.put('/{product_id}', response_model=ProductResponse)
async def update_product(product_id: UUID, payload: ProductUpdate):
    product = await product_service.update(product_id, payload)
    if not product:
        raise HTTPException(404, 'Product not found')
    return await product_service.get(product_id)

@router.delete('/{product_id}')
async def delete_product(product_id: UUID):
    success = await product_service.delete(product_id)
    if not success:
        raise HTTPException(404, 'Product not found')
    return {'status': 'deleted'}
