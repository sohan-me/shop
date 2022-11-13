from django.urls import path
from . import views


app_name = 'accounts'

urlpatterns = [

	path('register/', views.register, name='register'),
	path('log_in/', views.log_in, name='log_in'),
	path('log_out/', views.log_out, name='log_out'),

	
	path('activate/<uidb64>/<token>/', views.activate, name='activate'),
	path('dashboard/', views.dashboard, name='dashboard'),
	path('', views.dashboard, name='dashboard'),
]