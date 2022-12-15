from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [

	path('place_order/', views.place_order, name='place_order'),
	path('payment/', views.payment, name='payment'),
	path('order_completed/', views.order_completed, name='order_completed'),
	path('order_details/<int:order_id>/', views.order_details, name='order_details'),

]