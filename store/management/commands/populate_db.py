import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from store.models import Product, Cart, CartItem, Order, OrderItem, Shipment, Payment, Wishlist, Category

CustomUser = get_user_model()  # Ensure Django uses the correct custom user model


class Command(BaseCommand):
    help = "Populates the database with test data for frontend development"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Starting to populate the database..."))

        # 1. Create Test Users
        self.create_users()

        # 2. Create Products
        self.create_products()

        # 3. Create Carts and Cart Items
        self.create_carts()

        # 4. Create Orders and Order Items
        self.create_orders()

        # 5. Create Shipments
        self.create_shipments()

        # 6. Create Payments
        self.create_payments()

        # 7. Create Wishlists
        self.create_wishlists()

        self.stdout.write(self.style.SUCCESS("Database successfully populated! 🎉"))

    # ============================
    # USERS
    # ============================
    def create_users(self):
        self.stdout.write("Creating test users...")

        users_data = [
            {"username": "john_doe", "email": "john@example.com", "phone_number": "1234567890", "address": "123 Street, City"},
            {"username": "jane_doe", "email": "jane@example.com", "phone_number": "0987654321", "address": "456 Avenue, City"},
            {"username": "admin_user", "email": "admin@example.com", "phone_number": "1112223333", "address": "789 Road, City"},
        ]

        for user_data in users_data:
            user, created = CustomUser.objects.get_or_create(
                username=user_data["username"],
                defaults={
                    "email": user_data["email"],
                    "phone_number": user_data.get("phone_number", ""),
                    "address": user_data.get("address", ""),
                },
            )
            if created:
                user.set_password("password123")  # Set a default password
                user.save()

        self.stdout.write(self.style.SUCCESS("✅ Users created successfully!"))

    # ============================
    # PRODUCTS
    # ============================
    def create_products(self):
        self.stdout.write("Creating test categories and products...")

        # Create sample categories
        category_names = ["Floral", "Fresh", "Woody", "Citrus"]
        categories = {name: Category.objects.get_or_create(name=name)[0] for name in category_names}

        # Define test products and assign them to categories
        products_data = [
            {"name": "Vintage Rose", "description": "A classic rose perfume.", "price": 49.99, "stock": 50, "category": categories["Floral"]},
            {"name": "Ocean Breeze", "description": "A fresh ocean scent.", "price": 59.99, "stock": 40, "category": categories["Fresh"]},
            {"name": "Night Elegance", "description": "A mysterious and deep fragrance.", "price": 79.99, "stock": 30, "category": categories["Woody"]},
            {"name": "Citrus Zest", "description": "A vibrant citrus-based perfume.", "price": 39.99, "stock": 60, "category": categories["Citrus"]},
        ]

        for product_data in products_data:
            Product.objects.get_or_create(
                name=product_data["name"],
                defaults={
                    "description": product_data["description"],
                    "price": product_data["price"],
                    "stock": product_data["stock"],
                    "category": product_data["category"]
                }
            )

        self.stdout.write(self.style.SUCCESS("✅ Categories and products created successfully!"))


    # ============================
    # CARTS
    # ============================
    def create_carts(self):
        self.stdout.write("Creating carts and adding items...")

        users = CustomUser.objects.all()
        products = Product.objects.all()

        for user in users:
            cart, created = Cart.objects.get_or_create(user=user)
            for _ in range(random.randint(1, 3)):  # Add 1-3 items per cart
                product = random.choice(products)
                CartItem.objects.get_or_create(cart=cart, product=product, defaults={"quantity": random.randint(1, 5)})

        self.stdout.write(self.style.SUCCESS("✅ Carts populated successfully!"))

    # ============================
    # ORDERS
    # ============================
    def create_orders(self):
        self.stdout.write("Creating test orders...")

        users = CustomUser.objects.all()
        products = Product.objects.all()

        for user in users:
            if random.choice([True, False]):  # 50% chance to create an order
                order = Order.objects.create(
                    user=user,
                    shipping_address=user.address or "Default Address",
                    total_price=random.randint(50, 200),
                    status=random.choice(["Pending", "Processing", "Shipped", "Delivered"])
                )

                for _ in range(random.randint(1, 3)):  # Add 1-3 items per order
                    product = random.choice(products)
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=random.randint(1, 3),
                        price_at_time_of_order=product.price
                    )

        self.stdout.write(self.style.SUCCESS("✅ Orders populated successfully!"))

    # ============================
    # SHIPMENTS
    # ============================
    def create_shipments(self):
        self.stdout.write("Creating test shipments...")

        orders = Order.objects.filter(status__in=["Shipped", "Delivered"])

        for order in orders:
            Shipment.objects.get_or_create(
                order=order,
                tracking_number=f"TRACK-{random.randint(1000,9999)}",
                status=order.status,
                estimated_delivery_date="2024-06-30",
            )

        self.stdout.write(self.style.SUCCESS("✅ Shipments created successfully!"))

    # ============================
    # PAYMENTS
    # ============================
    def create_payments(self):
        self.stdout.write("Creating test payments...")

        orders = Order.objects.filter(status__in=["Processing", "Shipped", "Delivered"])

        for order in orders:
            Payment.objects.get_or_create(
                order=order,
                amount=order.total_price,
                payment_method=random.choice(["Credit Card", "PayPal", "Bank Transfer"]),
                payment_status="Completed",
                transaction_id=f"TXN-{random.randint(10000,99999)}"
            )

        self.stdout.write(self.style.SUCCESS("✅ Payments created successfully!"))

    # ============================
    # WISHLISTS
    # ============================
    def create_wishlists(self):
        self.stdout.write("Creating wishlists...")

        users = CustomUser.objects.all()
        products = Product.objects.all()

        for user in users:
            wishlist, created = Wishlist.objects.get_or_create(user=user)
            for _ in range(random.randint(1, 3)):  # Add 1-3 products per wishlist
                product = random.choice(products)
                wishlist.products.add(product)

        self.stdout.write(self.style.SUCCESS("✅ Wishlists populated successfully!"))
