from django.contrib import admin
from .models import Category, Product, Order, OrderItem, Cart, CartItem, Wishlist, Payment, Shipment

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'price', 'stock')
    search_fields = ('name', 'category__name')
    list_filter = ('category',)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'total_price', 'status', 'created_at')
    search_fields = ('customer__user__username',)
    list_filter = ('status', 'created_at')

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'quantity', 'price')

class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer')

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart', 'product', 'quantity')

class WishlistAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'product')

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'order', 'payment_method', 'payment_status', 'created_at')
    list_filter = ('payment_status', 'payment_method')

class ShipmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'order', 'shipment_date', 'is_delivered')
    list_filter = ('is_delivered',)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Wishlist, WishlistAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Shipment, ShipmentAdmin)
