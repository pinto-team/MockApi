import random
from uuid import uuid4
from faker import Faker

from app.db.mongo import db

fake = Faker()

async def seed_data():
    # Stores
    if await db['stores'].count_documents({}) == 0:
        stores = []
        for _ in range(100):
            dt = fake.date_time_this_year()
            stores.append({'_id': str(uuid4()), 'name': fake.company(), 'created_at': dt, 'updated_at': dt})
        await db['stores'].insert_many(stores)
    store_ids = [doc['_id'] async for doc in db['stores'].find({}, {'_id':1})]

    # Categories
    if await db['categories'].count_documents({}) == 0:
        categories = []
        for _ in range(100):
            dt = fake.date_time_this_year()
            categories.append({'_id': str(uuid4()), 'name': fake.word().capitalize(), 'created_at': dt, 'updated_at': dt})
        await db['categories'].insert_many(categories)
    category_ids = [doc['_id'] async for doc in db['categories'].find({}, {'_id':1})]

    # Brands
    if await db['brands'].count_documents({}) == 0:
        brands = []
        for _ in range(100):
            dt = fake.date_time_this_year()
            brands.append({'_id': str(uuid4()), 'name': fake.company(), 'created_at': dt, 'updated_at': dt})
        await db['brands'].insert_many(brands)
    brand_ids = [doc['_id'] async for doc in db['brands'].find({}, {'_id':1})]

    # Warehouses
    if await db['warehouses'].count_documents({}) == 0:
        warehouses = []
        for _ in range(100):
            dt = fake.date_time_this_year()
            warehouses.append({'_id': str(uuid4()), 'name': f"Warehouse {_}", 'location': fake.city(), 'created_at': dt, 'updated_at': dt})
        await db['warehouses'].insert_many(warehouses)
    warehouse_ids = [doc['_id'] async for doc in db['warehouses'].find({}, {'_id':1})]

    # Products and Images
    if await db['products'].count_documents({}) == 0:
        products = []
        images = []
        for _ in range(100):
            pid = str(uuid4())
            dt = fake.date_time_this_year()
            product = {
                '_id': pid,
                'sku': fake.unique.bothify(text='???-########').upper(),
                'name': fake.word().capitalize(),
                'price': round(random.uniform(1, 100), 2),
                'attributes': {'color': fake.color_name()},
                'stock': random.randint(0, 100),
                'store_id': random.choice(store_ids),
                'category_id': random.choice(category_ids),
                'brand_id': random.choice(brand_ids),
                'warehouse_availability': [
                    {'warehouse_id': wid, 'stock': random.randint(0, 100)}
                    for wid in random.sample(warehouse_ids, k=random.randint(1, min(4, len(warehouse_ids))))
                ],
                'created_at': dt,
                'updated_at': dt,
            }
            products.append(product)
            for _ in range(random.randint(1,4)):
                images.append({
                    '_id': str(uuid4()),
                    'product_id': pid,
                    'url': f"https://picsum.photos/seed/{uuid4()}/200/300"
                })
        if products:
            await db['products'].insert_many(products)
        if images:
            await db['images'].insert_many(images)
