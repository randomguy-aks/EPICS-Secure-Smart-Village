
from django.urls import path
from . import views

urlpatterns = [
    # Seller URLs
    path('seller/register/', views.seller_register, name='seller_register'),
    path('seller/login/', views.seller_login, name='seller_login'),
    path('seller/logout/', views.seller_logout, name='seller_logout'),

    # Consumer URLs
    path('consumer/register/', views.consumer_register, name='consumer_register'),
    path('consumer/login/', views.consumer_login, name='consumer_login'),
    path('consumer/logout/', views.consumer_logout, name='consumer_logout'),
]
