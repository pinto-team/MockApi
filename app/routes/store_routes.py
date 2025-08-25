from fastapi import APIRouter, HTTPException
from uuid import UUID
from typing import List

from app.models.store import Store, StoreCreate, StoreUpdate
from app.services.store_service import store_service

router = APIRouter()

@router.get('/', response_model=List[Store])
async def list_stores():
    return await store_service.list()

@router.get('/{store_id}', response_model=Store)
async def get_store(store_id: UUID):
    store = await store_service.get(store_id)
    if not store:
        raise HTTPException(404, 'Store not found')
    return store

@router.post('/', response_model=Store)
async def create_store(payload: StoreCreate):
    return await store_service.create(payload)

@router.put('/{store_id}', response_model=Store)
async def update_store(store_id: UUID, payload: StoreUpdate):
    store = await store_service.update(store_id, payload)
    if not store:
        raise HTTPException(404, 'Store not found')
    return store

@router.delete('/{store_id}')
async def delete_store(store_id: UUID):
    success = await store_service.delete(store_id)
    if not success:
        raise HTTPException(404, 'Store not found')
    return {'status': 'deleted'}
