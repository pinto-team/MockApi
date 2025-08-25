from __future__ import annotations

from typing import List
from uuid import uuid4, UUID
import random

from faker import Faker

from app.models.product import (
    ProductCreate,
    PricingTier,
    WarehouseAvailability,
    Attributes,
    Dimensions,
)
from app.models.user import UserCreate

fake = Faker()

# -----------------------------
# Constants
# -----------------------------
CURRENCIES: List[str] = ["USD", "EUR", "QAR", "AED", "SAR"]
UOMS: List[str] = ["unit", "pack", "case"]
BRANDS: List[str] = ["FreshFarm", "Golden", "DailyChoice", "EcoPure", "SunDrop", "HappyCow"]

CATEGORIES: List[UUID] = [uuid4() for _ in range(8)]
WAREHOUSES: List[UUID] = [uuid4() for _ in range(3)]
SELLERS: List[UUID] = [uuid4() for _ in range(5)]

__all__ = [
    "fake_product_create",
    "fake_user_create",
    "set_seed",
]


# -----------------------------
# Utilities
# -----------------------------
def set_seed(seed: int | None = None) -> None:
    """
    Optionally set deterministic seeds for reproducible fakes.
    """
    if seed is None:
        return
    random.seed(seed)
    Faker.seed(seed)


def _fake_pricing_tiers(base_price: float) -> List[PricingTier]:
    """
    Create 2–3 tiered prices below base_price with small discounts.
    Some tiers may be omitted randomly to add variety.
    """
    tiers: List[PricingTier] = []
    for min_qty, disc in [(12, 0.03), (48, 0.07), (120, 0.12)]:
        if random.random() < 0.9:  # 90% chance to include this tier
            tiers.append(
                PricingTier(min_qty=min_qty, unit_price=round(base_price * (1 - disc), 2))
            )
    return tiers


def _fake_images() -> List[str]:
    """
    Generate between 1 and 4 placeholder images from picsum.photos.
    Always at least 1, up to 4, with cache-busting random param.
    """
    count = random.randint(1, 4)
    sizes = [(320, 240), (400, 300), (640, 480)]
    images: List[str] = []
    for _ in range(count):
        w, h = random.choice(sizes)
        cb = random.randint(1, 999999)
        images.append(f"https://picsum.photos/{w}/{h}?random={cb}")
    return images



# -----------------------------
# Factories
# -----------------------------
def fake_product_create() -> ProductCreate:
    """
    Build a ProductCreate payload with realistic wholesale fields.
    Includes:
      - pricing_tiers
      - warehouse_availability
      - attributes (weight/dimensions/packaging/storage/shelf_life/halal)
      - images (1..4 placekitten URLs)
    """
    base_price = round(random.uniform(0.5, 25.0), 2)
    purchase = round(base_price * random.uniform(0.6, 0.9), 2)
    sku = f"{fake.bothify(text='??-#####').upper()}"

    return ProductCreate(
        seller_id=random.choice(SELLERS),
        warehouse_id=random.choice(WAREHOUSES),
        sku=sku,
        name=f"{fake.word().title()} {fake.word().title()}",
        description=fake.sentence(nb_words=12),
        category_id=random.choice(CATEGORIES),
        brand=random.choice(BRANDS),
        base_price=base_price,
        purchase_price=purchase,
        currency=random.choice(CURRENCIES),
        tax_rate=random.choice([0, 0.05, 0.1]),
        min_order_quantity=random.choice([1, 6, 12, 24]),
        min_order_multiple=random.choice([None, 6, 12, 24]),
        stock=random.randint(0, 1000),
        warehouse_availability=[
            WarehouseAvailability(
                warehouse_id=random.choice(WAREHOUSES),
                stock=random.randint(0, 600),
                lead_time_days=random.randint(0, 5),
            )
        ],
        pricing_tiers=_fake_pricing_tiers(base_price),
        uom=random.choice(UOMS),
        pack_size=random.choice([None, 4, 6, 8, 12]),
        case_size=random.choice([None, 2, 4, 6]),
        barcode="".join([str(random.randint(0, 9)) for _ in range(13)]),
        attributes=Attributes(
            weight=round(random.uniform(0.1, 5.0), 2),
            dimensions=Dimensions(
                length=round(random.uniform(5, 40), 1),
                width=round(random.uniform(5, 40), 1),
                height=round(random.uniform(5, 40), 1),
            ),
            packaging=random.choice(["PET bottle", "TetraPak", "Glass jar", "Pouch"]),
            storage=random.choice(["ambient", "chilled", "frozen"]),
            shelf_life_days=random.choice([90, 180, 365]),
            halal=random.choice([True, False]),
        ),
        allow_backorder=random.choice([True, False]),
        is_active=random.choice([True, True, True, False]),
        images=_fake_images(),  # <- placekitten, 1..4 URLs
        tags=random.sample(
            ["organic", "promo", "local", "imported", "bulk"],
            k=random.randint(0, 3),
        ),
    )


def fake_user_create() -> UserCreate:
    """
    Build a minimal UserCreate payload.
    """
    return UserCreate(
        name=fake.name(),
        email=fake.unique.email(),
        role=random.choice(["buyer", "seller", "admin"]),
        is_active=random.choice([True, True, True, False]),
    )
