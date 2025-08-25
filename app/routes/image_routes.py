from fastapi import APIRouter, HTTPException
from uuid import UUID
from typing import List

from app.models.image import Image, ImageCreate, ImageUpdate
from app.services.image_service import image_service

router = APIRouter()

@router.get('/', response_model=List[Image])
async def list_images():
    return await image_service.list()

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
