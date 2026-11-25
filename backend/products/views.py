
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import transaction

from accounts.models import AccountProfile
from sellers.models import SellerProfile
from inventory.models import Inventory
from .models import Product
from .forms import ProductForm


def home(request):
    products = Product.objects.filter(
        status='published',
        seller__is_active=True
    ).select_related(
        'seller',
        'category'
    ).order_by('-created_at')

    return render(
        request,
        'products/home.html',
        {'products': products}
    )


@login_required
def add_product(request):
    account = AccountProfile.objects.filter(
        user=request.user,
        role='seller'
    ).first()

    if not account:
        return redirect('home')

    seller = SellerProfile.objects.filter(
        user=request.user,
        is_active=True
    ).first()

    if not seller:
        return redirect('home')

    if request.method == 'POST':
        form = ProductForm(request.POST)

        if form.is_valid():
            with transaction.atomic():
                product = form.save(commit=False)
                product.seller = seller
                product.status = 'published'
                product.save()

                Inventory.objects.create(
                    product=product,
                    quantity=form.cleaned_data['quantity']
                )

            return redirect('seller_dashboard')

    else:
        form = ProductForm()

    return render(
        request,
        'products/add_product.html',
        {'form': form}
    )


def product_detail(request, product_id):
    product = get_object_or_404(
        Product.objects.select_related('seller', 'category'),
        id=product_id,
        status='published',
        seller__is_active=True
    )

    inventory = Inventory.objects.filter(
        product=product
    ).first()

    return render(
        request,
        'products/product_detail.html',
        {
            'product': product,
            'inventory': inventory
        }
    )
