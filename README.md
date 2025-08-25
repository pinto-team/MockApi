# Mock API (FastAPI + MongoDB)

A small FastAPI project that uses MongoDB for persistence. On startup the
application seeds fake data with [Faker](https://faker.readthedocs.io/) and
exposes CRUD endpoints for several resources.

## Resources

| Resource   | Endpoint      |
|------------|---------------|
| Products   | `/products`   |
| Stores     | `/stores`     |
| Categories | `/categories` |
| Brands     | `/brands`     |
| Warehouses | `/warehouses` |
| Images     | `/images`     |

Products are linked to stores, categories, brands, warehouses and images. When
a collection is empty the application generates about 100 fake documents and
stores them in MongoDB. Image URLs are sourced from `picsum.photos`.

## Quickstart

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export MONGO_URL="mongodb://localhost:27017"
export MONGO_DB="mockapi"
uvicorn main:app --reload
```

Open http://127.0.0.1:8000/docs to explore the interactive API documentation.
