from django.contrib import admin
from .models import Payment, Order, OrderProduct
# Register your models here.

class OrderProductInline(admin.TabularInline):
	model = OrderProduct
	readonly_fields = ['payment', 'order', 'user', 'quantity', 'product_price', 'is_ordered']
	extra = 0
class AdminPaymentView(admin.ModelAdmin):
	
	list_display = ['payment_id', 'user', 'payment_method', 'amount_paid', 'status', 'created_at']
	list_filter = ['status']



class AdminOrderView(admin.ModelAdmin):

	list_display = ['order_number', 'user', 'first_name', 'last_name', 'status', 'ip', 'is_ordered', 'created_at', 'updated_at']
	list_filter = ['ip', 'is_ordered', 'user']
	search_fields = ['order_number', 'first_name', 'last_name', 'phone', 'email']
	inlines = [OrderProductInline]
	list_per_page = 20

class AdminOrderProductView(admin.ModelAdmin):

	list_display = ['product', 'payment', 'quantity', 'is_ordered', 'created_at', 'updated_at']
	list_filter = ['is_ordered', 'payment', 'product']
	list_editable = ['is_ordered']





admin.site.register(Payment, AdminPaymentView)
admin.site.register(Order, AdminOrderView)
admin.site.register(OrderProduct, AdminOrderProductView)