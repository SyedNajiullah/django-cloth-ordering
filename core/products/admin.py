from django.contrib import admin
from .models import Brand, Category, Product, ProductSize, ProductImage

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')

class ProductSizeInline(admin.TabularInline):
    model = ProductSize
    extra = 1

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'category', 'price', 'is_on_sale')
    list_filter = ('brand', 'category', 'is_on_sale')
    search_fields = ('name', 'sku')
    inlines = [ProductSizeInline, ProductImageInline]
