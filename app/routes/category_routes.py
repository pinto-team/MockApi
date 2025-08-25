from fastapi import APIRouter, HTTPException
from uuid import UUID
from typing import List

from app.models.category import Category, CategoryCreate, CategoryUpdate
from app.services.category_service import category_service

router = APIRouter()

@router.get('/', response_model=List[Category])
async def list_categories():
    return await category_service.list()

@router.get('/{category_id}', response_model=Category)
async def get_category(category_id: UUID):
    category = await category_service.get(category_id)
    if not category:
        raise HTTPException(404, 'Category not found')
    return category

@router.post('/', response_model=Category)
async def create_category(payload: CategoryCreate):
    return await category_service.create(payload)

@router.put('/{category_id}', response_model=Category)
async def update_category(category_id: UUID, payload: CategoryUpdate):
    category = await category_service.update(category_id, payload)
    if not category:
        raise HTTPException(404, 'Category not found')
    return category

@router.delete('/{category_id}')
async def delete_category(category_id: UUID):
    success = await category_service.delete(category_id)
    if not success:
        raise HTTPException(404, 'Category not found')
    return {'status': 'deleted'}
