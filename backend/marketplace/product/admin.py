from django.contrib import admin
from .models import Category, Product
from order.models import OrderItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['parent', 'name', 'slug']
    # list_editable = []
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'regular_price', 'in_sale', 'discount_price']
    list_filter = ['category', 'regular_price', 'discount_price', 'in_sale']
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(OrderItem)