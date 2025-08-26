from fastapi import APIRouter, HTTPException
from typing import List
from uuid import UUID

from app.models.user import User, UserCreate, UserUpdate
from app.services.user_service import user_service

router = APIRouter()


@router.get("/", response_model=List[User])
async def list_users():
    return await user_service.list()


@router.get("/{user_id}", response_model=User)
async def get_user(user_id: UUID):
    user = await user_service.get(user_id)
    if not user:
        raise HTTPException(404, "User not found")
    return user


@router.post("/", response_model=User)
async def create_user(payload: UserCreate):
    # در آینده می‌تونیم اینجا رمز رو هش کنیم
    return await user_service.create(payload)


@router.put("/{user_id}", response_model=User)
async def update_user(user_id: UUID, payload: UserUpdate):
    user = await user_service.update(user_id, payload)
    if not user:
        raise HTTPException(404, "User not found")
    return user


@router.delete("/{user_id}")
async def delete_user(user_id: UUID):
    success = await user_service.delete(user_id)
    if not success:
        raise HTTPException(404, "User not found")
    return {"status": "deleted"}
