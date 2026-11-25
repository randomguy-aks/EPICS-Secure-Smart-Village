
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.views.decorators.http import require_POST

from accounts.models import AccountProfile
from products.models import Product
from inventory.models import Inventory
from .models import Cart, CartItem


def is_consumer(user):
    return AccountProfile.objects.filter(
        user=user,
        role='consumer'
    ).exists()


@login_required
@require_POST
def add_to_cart(request, product_id):
    if not is_consumer(request.user):
        messages.error(request, 'Only consumers can add products to their cart.')
        return redirect('home')

    product = get_object_or_404(
        Product,
        id=product_id,
        status='published',
        seller__is_active=True
    )

    inventory = Inventory.objects.filter(product=product).first()

    if not inventory or inventory.quantity < 1:
        messages.error(request, 'This product is currently out of stock.')
        return redirect('product_detail', product_id=product.id)

    cart, created = Cart.objects.get_or_create(
        consumer=request.user
    )

    with transaction.atomic():
        item = CartItem.objects.select_for_update().filter(
            cart=cart,
            product=product
        ).first()

        current_quantity = item.quantity if item else 0

        if current_quantity + 1 > inventory.quantity:
            messages.error(request, 'Not enough stock available.')
            return redirect('product_detail', product_id=product.id)

        if item:
            item.quantity += 1
            item.save()
        else:
            CartItem.objects.create(
                cart=cart,
                product=product,
                quantity=1
            )

    messages.success(request, 'Product added to your cart!')
    return redirect('cart')


@login_required
def cart_view(request):
    if not is_consumer(request.user):
        return redirect('home')

    cart = Cart.objects.filter(
        consumer=request.user
    ).first()

    return render(
        request,
        'orders/cart.html',
        {'cart': cart}
    )


@login_required
@require_POST
def update_cart_quantity(request, item_id):
    if not is_consumer(request.user):
        return redirect('home')

    cart = Cart.objects.filter(
        consumer=request.user
    ).first()

    if not cart:
        return redirect('cart')

    item = get_object_or_404(
        CartItem,
        id=item_id,
        cart=cart
    )

    action = request.POST.get('action')

    if action == 'increase':
        inventory = Inventory.objects.filter(
            product=item.product
        ).first()

        if not inventory or item.quantity >= inventory.quantity:
            messages.error(request, 'Maximum available stock reached.')
            return redirect('cart')

        item.quantity += 1
        item.save()

    elif action == 'decrease':
        if item.quantity > 1:
            item.quantity -= 1
            item.save()
        else:
            messages.warning(
                request,
                'Please confirm removal of this product.'
            )

    return redirect('cart')


@login_required
@require_POST
def remove_from_cart(request, item_id):
    if not is_consumer(request.user):
        return redirect('home')

    cart = Cart.objects.filter(
        consumer=request.user
    ).first()

    if not cart:
        return redirect('cart')

    item = get_object_or_404(
        CartItem,
        id=item_id,
        cart=cart
    )

    item.delete()

    messages.success(request, 'Product removed from your cart.')

    return redirect('cart')
