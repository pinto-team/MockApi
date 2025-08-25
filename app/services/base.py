from __future__ import annotations
from typing import Any, Callable, Dict, List, Optional, Type
from uuid import UUID, uuid4
from datetime import datetime

class InMemoryCRUD:
    """Generic in-memory CRUD with pagination, filtering, search and soft delete.
    Expects Pydantic models for Model/Create/Update.
    """
    def __init__(self, *, model_cls: Type, create_cls: Type, update_cls: Type,
                 search_fields: Optional[List[str]] = None,
                 unique_fields: Optional[List[str]] = None,
                 sortable_fields: Optional[List[str]] = None):
        self.model_cls = model_cls
        self.create_cls = create_cls
        self.update_cls = update_cls
        self.search_fields = search_fields or []
        self.unique_fields = unique_fields or []
        self.sortable_fields = set(sortable_fields or [])
        self._store: Dict[UUID, Any] = {}

    # ---- utils ----
    def _check_unique(self, data: Dict[str, Any], exclude_id: Optional[UUID] = None):
        for field in self.unique_fields:
            if field not in data:
                continue
            value = data[field]
            for _id, obj in self._store.items():
                if exclude_id and _id == exclude_id:
                    continue
                if getattr(obj, field, None) == value:
                    raise ValueError(f"{field} already exists")

    def _apply_filters(self, items: List[Any], filters: Dict[str, Any]) -> List[Any]:
        if not filters:
            return items
        def match(obj):
            for k, v in filters.items():
                if not hasattr(obj, k):
                    return False
                if str(getattr(obj, k)) != str(v):
                    return False
            return True
        return [o for o in items if match(o)]

    def _apply_search(self, items: List[Any], q: Optional[str]) -> List[Any]:
        if not q:
            return items
        ql = str(q).lower()
        def hit(o):
            for f in self.search_fields:
                val = getattr(o, f, None)
                if val and ql in str(val).lower():
                    return True
            return False
        return [o for o in items if hit(o)]

    # ---- CRUD ----
    def create(self, payload) -> Any:
        data = payload.model_dump()
        self._check_unique(data)
        obj = self.model_cls(**data)
        self._store[obj.id] = obj
        return obj

    def list(self, *, page:int=1, limit:int=20, q:Optional[str]=None,
             sort_by:Optional[str]=None, order:str="asc",
             filters: Optional[Dict[str, Any]] = None):
        items = list(self._store.values())
        # soft-delete aware: if model has is_active, default only active
        only_active = True
        if only_active and items and hasattr(items[0], "is_active"):
            items = [i for i in items if getattr(i, "is_active")]
        # filters & search
        items = self._apply_filters(items, filters or {})
        items = self._apply_search(items, q)
        # sorting
        if sort_by and (not self.sortable_fields or sort_by in self.sortable_fields):
            reverse = (order == "desc")
            items.sort(key=lambda x: getattr(x, sort_by, None), reverse=reverse)
        total = len(items)
        start = (page-1) * limit
        end = start + limit
        return items[start:end], total

    def get(self, id_: UUID):
        return self._store.get(id_)

    def update(self, id_: UUID, patch) -> Any:
        obj = self._store.get(id_)
        if not obj:
            return None
        data = patch.model_dump(exclude_unset=True)
        if not data:
            return obj
        self._check_unique(data, exclude_id=id_)
        for k, v in data.items():
            setattr(obj, k, v)
        if hasattr(obj, "updated_at"):
            setattr(obj, "updated_at", datetime.utcnow())
        self._store[id_] = obj
        return obj

    def delete(self, id_: UUID, hard: bool=False):
        obj = self._store.get(id_)
        if not obj:
            return None
        if hard:
            self._store.pop(id_, None)
            return True
        # soft toggle if has is_active
        if hasattr(obj, "is_active"):
            obj.is_active = not bool(obj.is_active)
            if hasattr(obj, "updated_at"):
                setattr(obj, "updated_at", datetime.utcnow())
            return obj
        # else do hard delete
        self._store.pop(id_, None)
        return True
