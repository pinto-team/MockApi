from faker import Faker
from uuid import uuid4
import random
from app.models.product import ProductCreate, PricingTier, WarehouseAvailability, Attributes, Dimensions
from app.models.user import UserCreate

fake = Faker()

CURRENCIES = ["USD","EUR","QAR","AED","SAR"]
UOMS = ["unit","pack","case"]
BRANDS = ["FreshFarm","Golden","DailyChoice","EcoPure","SunDrop","HappyCow"]

CATEGORIES = [uuid4() for _ in range(8)]
WAREHOUSES = [uuid4() for _ in range(3)]
SELLERS = [uuid4() for _ in range(5)]

def fake_product_create() -> ProductCreate:
    base_price = round(random.uniform(0.5, 25.0), 2)
    purchase = round(base_price * random.uniform(0.6, 0.9), 2)
    sku = f"{fake.bothify(text='??-#####').upper()}"
    pricing = []
    for min_qty, disc in [(12, 0.03), (48, 0.07), (120, 0.12)]:
        if random.random() < 0.9:
            pricing.append(PricingTier(min_qty=min_qty, unit_price=round(base_price*(1-disc),2)))
    return ProductCreate(
        seller_id=random.choice(SELLERS),
        warehouse_id=random.choice(WAREHOUSES),
        sku=sku,
        name=fake.word().title() + " " + fake.word().title(),
        description=fake.sentence(nb_words=12),
        category_id=random.choice(CATEGORIES),
        brand=random.choice(BRANDS),
        base_price=base_price,
        purchase_price=purchase,
        currency=random.choice(CURRENCIES),
        tax_rate=random.choice([0, 0.05, 0.1]),
        min_order_quantity=random.choice([1,6,12,24]),
        min_order_multiple=random.choice([None,6,12,24]),
        stock=random.randint(0, 1000),
        warehouse_availability=[
            WarehouseAvailability(warehouse_id=random.choice(WAREHOUSES), stock=random.randint(0,600), lead_time_days=random.randint(0,5))
        ],
        pricing_tiers=pricing,
        uom=random.choice(UOMS),
        pack_size=random.choice([None,4,6,8,12]),
        case_size=random.choice([None,2,4,6]),
        barcode="".join([str(random.randint(0,9)) for _ in range(13)]),
        attributes=Attributes(
            weight=round(random.uniform(0.1, 5.0), 2),
            dimensions=Dimensions(length=round(random.uniform(5,40),1), width=round(random.uniform(5,40),1), height=round(random.uniform(5,40),1)),
            packaging=random.choice(["PET bottle","TetraPak","Glass jar","Pouch"]),
            storage=random.choice(["ambient","chilled","frozen"]),
            shelf_life_days=random.choice([90,180,365]),
            halal=random.choice([True, False])
        ),
        allow_backorder=random.choice([True, False]),
        is_active=random.choice([True, True, True, False]),
        images=[fake.image_url(width=640, height=480)],
        tags=random.sample(["organic","promo","local","imported","bulk"], k=random.randint(0,3))
    )

def fake_user_create() -> UserCreate:
    return UserCreate(
        name=fake.name(),
        email=fake.unique.email(),
        role=random.choice(["buyer","seller","admin"]),
        is_active=random.choice([True, True, True, False])
    )
