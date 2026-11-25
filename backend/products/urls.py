
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path(
        'seller/products/add/',
        views.add_product,
        name='add_product'
    ),

    path(
        'product/<int:product_id>/',
        views.product_detail,
        name='product_detail'
    ),
]
