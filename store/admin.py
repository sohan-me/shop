from django.contrib import admin
from .models import Product, Variation
# Register your models here.


class AdminProductView(admin.ModelAdmin):

    prepopulated_fields = {'slug': ('product_name',)}
    list_display = ['product_name', 'price', 'stock', 'category', 'modified_date', 'is_available']
    list_editable = ['is_available']
    list_filter = ['category', 'is_available']

class AdminVariationView(admin.ModelAdmin):

    list_display = ['product','variation_category', 'variation_value', 'is_available']
    list_editable = ['is_available']
    list_filter = ['product','variation_category', 'is_available']


admin.site.register(Product, AdminProductView)
admin.site.register(Variation, AdminVariationView)
