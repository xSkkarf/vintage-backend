import random
from django.core.management.base import BaseCommand
from users.models import User, Customer
from store.models import Category, Product, Order, OrderItem, Payment, Shipment
from django.utils.timezone import now

class Command(BaseCommand):
    help = "Populate the database with dummy data"

    def handle(self, *args, **kwargs):
        self.stdout.write("🚀 Populating the database with dummy data...")

        # Create Admin User
        admin_user, created = User.objects.get_or_create(
            username="admin",
            defaults={"email": "admin@example.com", "is_staff": True, "is_superuser": True}
        )
        if created:
            admin_user.set_password("admin123")
            admin_user.save()
        
        # Create Customers
        customers = []
        for i in range(5):
            user = User.objects.create_user(
                username=f"user{i+1}",
                email=f"user{i+1}@example.com",
                password="password123",
            )
            customer = Customer.objects.create(user=user, phone_number=f"12345678{i}", address=f"Address {i+1}")
            customers.append(customer)
        
        # Create Categories
        categories = ["Floral", "Woody", "Citrus", "Spicy"]
        category_objs = [Category.objects.create(name=cat) for cat in categories]

        # Create Products
        products = []
        for i in range(10):
            product = Product.objects.create(
                name=f"Perfume {i+1}",
                SKU=f"PRD00{i+1}",
                description=f"Description for perfume {i+1}",
                price=random.uniform(20, 150),
                stock=random.randint(5, 100),
                category=random.choice(category_objs),
            )
            products.append(product)

        # Create Orders
        for customer in customers:
            order = Order.objects.create(
                customer=customer,
                total_price=random.uniform(50, 300),
                status=random.choice(["pending", "shipped", "delivered"]),
                created_at=now()
            )
            for _ in range(random.randint(1, 3)):  # Add 1-3 items per order
                product = random.choice(products)
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=random.randint(1, 5),
                    price=product.price
                )
            
            # Create Payment
            Payment.objects.create(
                customer=customer,
                order=order,
                payment_method=random.choice(["card", "paypal"]),
                payment_status=random.choice(["pending", "completed"]),
                created_at=now()
            )

            # Create Shipment
            Shipment.objects.create(
                customer=customer,
                order=order,
                address=customer.address,
                city="Test City",
                state="Test State",
                country="Test Country",
                zip_code="12345",
                shipment_date=now(),
                is_delivered=random.choice([True, False])
            )

        self.stdout.write(self.style.SUCCESS("✅ Database populated successfully!"))

