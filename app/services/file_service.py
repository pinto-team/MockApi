from app.models.file import File, FileCreate, FileUpdate
from .base import MongoCRUD


class FileService(MongoCRUD):
    def __init__(self):
        super().__init__(
            collection="files",
            model_cls=File,
            create_cls=FileCreate,
            update_cls=FileUpdate
        )


file_service = FileService()
