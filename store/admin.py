from django.contrib import admin
from .models import Product, Cart, CartItem, Order, OrderItem, Shipment, Payment, Wishlist

# ============================
# Product Admin
# ============================
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'stock', 'created_at')
    search_fields = ('name',)
    list_filter = ('created_at', 'updated_at')
    ordering = ('-created_at',)


# ============================
# Cart Admin
# ============================
class CartItemInline(admin.TabularInline):  # Inline model for Cart Items
    model = CartItem
    extra = 1


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at')
    inlines = [CartItemInline]


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart', 'product', 'quantity')
    search_fields = ('cart__user__username', 'product__name')


# ============================
# Order Admin
# ============================
class OrderItemInline(admin.TabularInline):  # Inline model for Order Items
    model = OrderItem
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username',)
    ordering = ('-created_at',)
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'quantity', 'price_at_time_of_order')


# ============================
# Shipment Admin
# ============================
@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'tracking_number', 'status', 'estimated_delivery_date')
    list_filter = ('status',)
    search_fields = ('order__id', 'tracking_number')


# ============================
# Payment Admin
# ============================
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'amount', 'payment_method', 'payment_status', 'payment_date')
    list_filter = ('payment_status', 'payment_method')
    search_fields = ('order__id', 'transaction_id')


# ============================
# Wishlist Admin
# ============================
@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at')
    search_fields = ('user__username',)
