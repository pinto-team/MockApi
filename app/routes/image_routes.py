from fastapi import APIRouter, HTTPException, Query
from uuid import UUID
from typing import List, Optional

from app.models.image import Image, ImageCreate, ImageUpdate
from app.services.image_service import image_service

router = APIRouter()

@router.get('/', response_model=List[Image])
async def list_images(
    product_id: Optional[UUID] = Query(None, description="Filter images by product_id"),
    is_primary: Optional[bool] = Query(None, description="Filter by primary image"),
    search: Optional[str] = Query(None, description="Search in alt_text or url"),
    sort_by: Optional[str] = Query(None, description="Sort by 'sort_order' or 'created_at' (asc/desc)")
):
    images = await image_service.list()

    # فیلتر با product_id
    if product_id:
        images = [img for img in images if img.product_id == product_id]

    # فیلتر با is_primary
    if is_primary is not None:
        images = [img for img in images if img.is_primary == is_primary]

    # سرچ در alt_text یا url
    if search:
        images = [
            img for img in images
            if (img.alt_text and search.lower() in img.alt_text.lower())
            or search.lower() in img.url.lower()
        ]

    # مرتب‌سازی
    if sort_by:
        if sort_by == "sort_order":
            images = sorted(images, key=lambda i: i.sort_order or 0)
        elif sort_by == "sort_order_desc":
            images = sorted(images, key=lambda i: i.sort_order or 0, reverse=True)
        elif sort_by == "created_at":
            images = sorted(images, key=lambda i: i.created_at)
        elif sort_by == "created_at_desc":
            images = sorted(images, key=lambda i: i.created_at, reverse=True)

    return images

@router.get('/{image_id}', response_model=Image)
async def get_image(image_id: UUID):
    image = await image_service.get(image_id)
    if not image:
        raise HTTPException(404, 'Image not found')
    return image

@router.post('/', response_model=Image)
async def create_image(payload: ImageCreate):
    return await image_service.create(payload)

@router.put('/{image_id}', response_model=Image)
async def update_image(image_id: UUID, payload: ImageUpdate):
    image = await image_service.update(image_id, payload)
    if not image:
        raise HTTPException(404, 'Image not found')
    return image

@router.delete('/{image_id}')
async def delete_image(image_id: UUID):
    success = await image_service.delete(image_id)
    if not success:
        raise HTTPException(404, 'Image not found')
    return {'status': 'deleted'}
