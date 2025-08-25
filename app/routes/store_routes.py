from fastapi import APIRouter, HTTPException, Query
from uuid import UUID
from typing import List, Optional

from app.models.store import Store, StoreCreate, StoreUpdate
from app.services.store_service import store_service

router = APIRouter()

@router.get('/', response_model=List[Store])
async def list_stores(
    search: Optional[str] = Query(None, description="Search stores by name, address or phone"),
    sort_by: Optional[str] = Query(None, description="Sort by 'name' or 'created_at' (asc/desc)")
):
    stores = await store_service.list()

    # فیلتر با search
    if search:
        stores = [
            s for s in stores
            if search.lower() in s.name.lower()
            or (s.address and search.lower() in s.address.lower())
            or (s.phone and search.lower() in s.phone.lower())
        ]

    # مرتب‌سازی
    if sort_by:
        if sort_by == "name":
            stores = sorted(stores, key=lambda s: s.name)
        elif sort_by == "name_desc":
            stores = sorted(stores, key=lambda s: s.name, reverse=True)
        elif sort_by == "created_at":
            stores = sorted(stores, key=lambda s: s.created_at)
        elif sort_by == "created_at_desc":
            stores = sorted(stores, key=lambda s: s.created_at, reverse=True)

    return stores

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
