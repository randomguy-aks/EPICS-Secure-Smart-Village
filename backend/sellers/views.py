from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from accounts.models import AccountProfile
from .models import SellerProfile


@login_required
def seller_dashboard(request):
    account = AccountProfile.objects.filter(
        user=request.user,
        role='seller'
    ).first()

    if not account:
        return redirect('home')

    # Inactive seller profiles must not access seller-management pages.
    seller = SellerProfile.objects.filter(
        user=request.user,
        is_active=True
    ).first()

    if not seller:
        return redirect('home')

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
