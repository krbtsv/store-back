from django.contrib import admin
from django.utils.safestring import mark_safe

from products.models import ProductCategory, Product, Basket


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    list_display_links = ('id', 'name')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'price', 'quantity', 'category', 'get_image')
    list_display_links = ('id', 'name')

    def get_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="100">')
        return '-'

    get_image.short_description = 'Фото'


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_timestamp')
    list_display_links = ('id', 'user')
