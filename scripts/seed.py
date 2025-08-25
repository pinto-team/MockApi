#!/usr/bin/env python3
from app.services.product_service import product_service
from app.services.user_service import user_service
from app.services.faker_utils import fake_product_create, fake_user_create, set_seed
import os, sys

def main():
    n_products = int(os.getenv("SEED_PRODUCTS", "100"))
    n_users = int(os.getenv("SEED_USERS", "50"))
    if os.getenv("FAKER_SEED"):
        set_seed(int(os.getenv("FAKER_SEED")))

    for _ in range(n_products):
        product_service.create(fake_product_create())
    for _ in range(n_users):
        user_service.create(fake_user_create())
    print(f"Seeded products={n_products}, users={n_users}")

if __name__ == "__main__":
    sys.exit(main())
