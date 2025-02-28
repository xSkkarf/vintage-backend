from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Customer

class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'username', 'email', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email')

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'phone_number', 'address')
    search_fields = ('user__username', 'phone_number')

admin.site.register(User, CustomUserAdmin)
admin.site.register(Customer, CustomerAdmin)
