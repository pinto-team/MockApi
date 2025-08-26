import os
import uuid
import shutil
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse

from app.services.file_service import file_service
from app.models.file import FileCreate

router = APIRouter()
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@router.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    ext = file.filename.split(".")[-1].lower()
    allowed_ext = ["jpg", "jpeg", "png", "gif", "webp"]

    if ext not in allowed_ext:
        raise HTTPException(400, detail="فرمت فایل پشتیبانی نمی‌شود")

    file_name = f"{uuid.uuid4()}.{ext}"
    file_path = UPLOAD_DIR / file_name

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    url = f"/static/{file_name}"

    # رکورد در دیتابیس
    file_doc = FileCreate(
        url=url,
        filename=file.filename,
        content_type=file.content_type,
        size=file.spool_max_size
    )
    new_file = await file_service.create(file_doc)

    return JSONResponse(new_file.model_dump())
