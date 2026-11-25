
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Authentication
    path('accounts/', include('accounts.urls')),

    # Seller Dashboard
    path('seller/', include('sellers.urls')),

    # Shopping Cart and Orders
    path('orders/', include('orders.urls')),

    # Homepage and Products
    path('', include('products.urls')),
]
