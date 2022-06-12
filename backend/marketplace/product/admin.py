from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import *


from django.contrib import admin
from .models import Properties, Category, CategoryProperty

# class CategoryPropertyInline(admin.TabularInline):
#     model = CategoryProperty
#     extra = 1


class PropertiesToCategoriesInline(admin.TabularInline):
    model = CategoryProperty


class PropertiesAdmin(admin.ModelAdmin):
    inlines = [
        PropertiesToCategoriesInline,
    ]
    exclude = ["categories"]


class CategoryAdmin(MPTTModelAdmin):
    list_display = ['name', 'parent', 'properties']
    def list_of_properties(self, obj):
        return f"{','.join([prop.property_name for prop in obj.properies.all()])}"

    list_of_properties.short_description = 'Свойства категории'

    inlines = [
        PropertiesToCategoriesInline,
    ]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Properties, PropertiesAdmin)
# @admin.register(Properties)
# class PropertiesAdmin(admin.ModelAdmin):
#     list_display = ['property_name']
#     list_filter = ['categories__name']  # Enable filtering by category name
#     search_fields = ['property_name']  # Enable searching by property name
#     inlines = [CategoryPropertyInline]
#
# @admin.register(Category)
# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ['name']
#     inlines = [CategoryPropertyInline]
#
# @admin.register(CategoryProperty)
# class CategoryPropertyAdmin(admin.ModelAdmin):
#     list_display = ['category_id', 'property_name']
#     list_filter = ['category_id', 'property_name']
#     search_fields = ['category_id__name', 'property_name__property_name']
#
#
#
# class PropertiesInline(admin.TabularInline):
#     model = Category.properties.CategoryProperty
#     #model = Properties
#     extra = 0
#
# class CategoryAdmin(MPTTModelAdmin):
#     inlines = [
#         Properties
#     ]
#     #list_display = ['parent', 'name', 'slug']
#     prepopulated_fields = {'slug': ('name',)}
# #
# #
# #admin.site.register(Properties, PropertiesInline)
# admin.site.register(Category, CategoryAdmin)

# class ProductSpecificationInline(admin.TabularInline):
#     model = ProductSpecification
#
#
#
# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     inlines = [
#         ProductSpecificationInline
#     ]
#     list_display = ['title', 'slug', 'regular_price', 'in_sale', 'discount_price']
#     list_filter = ['category', 'regular_price', 'discount_price', 'in_sale']
#     prepopulated_fields = {'slug': ('title',)}
#
#
# admin.site.register(OrderItem)

# class ProductAdmin(admin.ModelAdmin):
#     #list_display = ['title', 'slug', 'regular_price', 'in_sale', 'discount_price']
#
#     #     list_filter = ['category', 'regular_price', 'discount_price', 'in_sale']
#     prepopulated_fields = {'slug': ('title',)}
#     def get_form(self, request, obj=None, **kwargs):
#         form = super(ProductAdmin, self).get_form(request, obj, **kwargs)
#         category = None
#         if obj:
#             category = obj.category
#         form.base_fields['category'].widget.attrs['onchange'] = 'display_specification_table(this.value);'
#         if category:
#             if category.name == 'Clothes':
#                 form.base_fields['specification'].queryset = ClothesSpecification.objects.filter(category=category)
#             elif category.name == 'Electronics':
#                 form.base_fields['specification'].queryset = ElectronicsSpecification.objects.filter(category=category)
#         return form
#
#
# admin.site.register(Product, ProductAdmin)

