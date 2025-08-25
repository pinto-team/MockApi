# Wholesale API (FastAPI + Faker)

A minimal scaffold to spin up **fake APIs** fast. Ships with `products` and `users` resources and a generic CRUD layer so you can add more resources in minutes.

## Quickstart
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Then open: http://127.0.0.1:8000/docs

## Add a new resource
1) Copy `app/models/product.py` to a new file, e.g. `app/models/warehouse.py`, and adapt fields.
2) Write a faker factory in `app/services/faker_utils.py` returning a `CreateModel` instance.
3) Create a router in `app/routes/<name>_routes.py` using the `build_crud_router` factory.
4) Include the new router in `app/main.py`.

> The generic CRUD service handles: list (filters + search + sort + pagination), get, create (unique fields), update, soft delete/reactivate, and optional seeding.


GET  http://localhost:8000/health

# Products
GET    http://localhost:8000/products
GET    http://localhost:8000/products/{id}
POST   http://localhost:8000/products
PUT    http://localhost:8000/products/{id}
DELETE http://localhost:8000/products/{id}
DELETE http://localhost:8000/products/{id}?hard=true
POST   http://localhost:8000/products/seed?n=5

# Users
GET    http://localhost:8000/users
GET    http://localhost:8000/users/{id}
POST   http://localhost:8000/users
PUT    http://localhost:8000/users/{id}
DELETE http://localhost:8000/users/{id}
DELETE http://localhost:8000/users/{id}?hard=true
POST   http://localhost:8000/users/seed?n=5
