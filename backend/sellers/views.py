
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from accounts.models import AccountProfile
from .models import SellerProfile


@login_required
def seller_dashboard(request):

    if not AccountProfile.objects.filter(
        user=request.user,
        role='seller'
    ).exists():
        return redirect('home')

    seller = SellerProfile.objects.get(user=request.user)

    products = seller.products.select_related(
        'category'
    ).order_by('-created_at')

    return render(
        request,
        'sellers/dashboard.html',
        {
            'seller': seller,
            'products': products
        }
    )
