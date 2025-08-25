from typing import Any, Callable, Dict, List, Optional, Type
from fastapi import APIRouter, HTTPException, Query, Request


def build_crud_router(*,
    resource_name: str,
    service,
    CreateModel: Type,
    UpdateModel: Type,
    Model: Type,
    allowed_filters: Optional[List[str]] = None,
    seed_fn: Optional[Callable[[int], int]] = None,
):
    router = APIRouter()
    _filters = set(allowed_filters or [])

    @router.get("/")
    def list_items(request: Request,
                   page: int = Query(1, ge=1),
                   limit: int = Query(20, ge=1, le=100),
                   q: Optional[str] = Query(None, description="search query"),
                   sort_by: Optional[str] = Query(None),
                   order: str = Query("asc")):
        qp = dict(request.query_params)
        filters: Dict[str, Any] = {k: v for k, v in qp.items() if (k in _filters)}
        items, total = service.list(page=page, limit=limit, q=q, sort_by=sort_by, order=order, filters=filters)
        return {
            "items": items,
            "pagination": {"page": page, "limit": limit, "total": total}
        }

    @router.get("/{item_id}")
    def get_item(item_id: str):
        obj = service.get(item_id)
        if not obj:
            # allow UUID string
            from uuid import UUID
            try:
                obj = service.get(UUID(item_id))
            except Exception:
                obj = None
        if not obj:
            raise HTTPException(status_code=404, detail=f"{resource_name} not found")
        return obj

    @router.post("/", status_code=201)
    def create_item(payload: CreateModel):
        try:
            obj = service.create(payload)
            return obj
        except ValueError as e:
            raise HTTPException(status_code=409, detail=str(e))

    @router.put("/{item_id}")
    def update_item(item_id: str, patch: UpdateModel):
        from uuid import UUID
        obj = service.get(item_id) or service.get(UUID(item_id)) if item_id else None
        if not obj:
            raise HTTPException(status_code=404, detail=f"{resource_name} not found")
        try:
            updated = service.update(obj.id, patch)
        except ValueError as e:
            raise HTTPException(status_code=409, detail=str(e))
        return updated

    @router.delete("/{item_id}")
    def delete_item(item_id: str, hard: bool = False):
        from uuid import UUID
        obj = service.get(item_id) or service.get(UUID(item_id)) if item_id else None
        if not obj:
            raise HTTPException(status_code=404, detail=f"{resource_name} not found")
        res = service.delete(obj.id, hard=hard)
        return {"message": "deleted" if res is True else ("toggled" if res else "not_found")}

    if seed_fn:
        @router.post("/seed")
        def seed(n: int = 30):
            added = seed_fn(n)
            return {"message": f"Seeded {added} {resource_name}", "count": added}

    return router
