from django.contrib import admin
from .models import Product, Variation, ReviewRating, ProductImage
import admin_thumbnails
# Register your models here.

@admin_thumbnails.thumbnail('images')
class ProductGalleryInline(admin.TabularInline):

    model = ProductImage
    extra = 1

class AdminProductView(admin.ModelAdmin):

    prepopulated_fields = {'slug': ('product_name',)}
    list_display = ['product_name', 'price', 'stock', 'category', 'modified_date', 'is_available']
    list_editable = ['is_available']
    list_filter = ['category', 'is_available']
    inlines = [ProductGalleryInline]

class AdminVariationView(admin.ModelAdmin):

    list_display = ['product','variation_category', 'variation_value', 'is_available']
    list_editable = ['is_available']
    list_filter = ['product','variation_category', 'is_available']

class AdminRatingView(admin.ModelAdmin):
    list_display = ['user', 'rating', 'product', 'ip', 'created_at']

admin.site.register(Product, AdminProductView)
admin.site.register(Variation, AdminVariationView)
admin.site.register(ReviewRating, AdminRatingView)