from pydantic import BaseModel, Field
from datetime import datetime
from typing import Any, Dict, List, Optional, Generic, TypeVar

T = TypeVar("T")


class ErrorDetail(BaseModel):
    field: Optional[str] = None
    message: str


class ApiErrorResponse(BaseModel):
    code: int
    message: str
    errors: List[ErrorDetail]
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


class PaginationMeta(BaseModel):
    page: int
    limit: int
    total: int
    total_pages: Optional[int] = None
    has_next: Optional[bool] = None
    has_previous: Optional[bool] = None


class SuccessMeta(BaseModel):
    message: str
    status: Optional[str] = "success"
    code: Optional[str] = "200"
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    trace_id: Optional[str] = None
    correlation_id: Optional[str] = None
    request_id: Optional[str] = None
    method: Optional[str] = None
    path: Optional[str] = None
    query: Optional[str] = None
    host: Optional[str] = None
    additional: Dict[str, Any] = {}
    pagination: Optional[PaginationMeta] = None


class ApiSuccessResponse(BaseModel, Generic[T]):
    data: Optional[T]
    meta: SuccessMeta
