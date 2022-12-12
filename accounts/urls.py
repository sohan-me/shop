from django.urls import path
from . import views


app_name = 'accounts'

urlpatterns = [

	path('register/', views.register, name='register'),
	path('log_in/', views.log_in, name='log_in'),
	path('log_out/', views.log_out, name='log_out'),
	path('reset_password/', views.reset_password, name='reset_password'),
	
	path('activate/<uidb64>/<token>/', views.activate, name='activate'),
	path('reset_password_validate/<uidb64>/<token>/', views.reset_password_validate, name='reset_password_validate'),
	path('reset_password_process/', views.reset_password_process, name='reset_password_process'),
	path('', views.dashboard, name='dashboard'),
	path('my_orders/', views.my_orders, name='my_orders'),
	path('edit_profile/', views.edit_profile, name='edit_profile'),
	path('change_password/', views.change_password, name='change_password'),
]