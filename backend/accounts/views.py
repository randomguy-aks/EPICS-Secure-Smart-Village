
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.http import require_POST
from django.db import transaction

from .forms import SellerRegistrationForm, ConsumerRegistrationForm
from .models import AccountProfile
from sellers.models import SellerProfile


def seller_register(request):
    if request.method == 'POST':
        form = SellerRegistrationForm(request.POST)

        if form.is_valid():
            with transaction.atomic():
                user = form.save()

                AccountProfile.objects.create(
                    user=user,
                    role='seller',
                    phone_number=form.cleaned_data['phone_number']
                )

                SellerProfile.objects.create(
                    user=user,
                    seller_type='individual',
                    business_name=form.cleaned_data['business_name'],
                    operating_location=form.cleaned_data['operating_location'],
                    description=form.cleaned_data['description']
                )

            login(request, user)
            return redirect('seller_dashboard')

    else:
        form = SellerRegistrationForm()

    return render(
        request,
        'accounts/seller_register.html',
        {'form': form}
    )


def seller_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()

            account = AccountProfile.objects.filter(
                user=user,
                role='seller'
            ).first()

            if account:
                login(request, user)
                return redirect('seller_dashboard')

            form.add_error(
                None,
                'This account is not registered as a seller.'
            )

    else:
        form = AuthenticationForm()

    return render(
        request,
        'accounts/seller_login.html',
        {'form': form}
    )


@login_required
@require_POST
def seller_logout(request):
    logout(request)
    return redirect('home')


def consumer_register(request):
    if request.method == 'POST':
        form = ConsumerRegistrationForm(request.POST)

        if form.is_valid():
            with transaction.atomic():
                user = form.save()

                AccountProfile.objects.create(
                    user=user,
                    role='consumer',
                    phone_number=form.cleaned_data['phone_number']
                )

            login(request, user)
            return redirect('home')

    else:
        form = ConsumerRegistrationForm()

    return render(
        request,
        'accounts/consumer_register.html',
        {'form': form}
    )


def consumer_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()

            account = AccountProfile.objects.filter(
                user=user,
                role='consumer'
            ).first()

            if account:
                login(request, user)
                return redirect('home')

            form.add_error(
                None,
                'This account is not registered as a consumer.'
            )

    else:
        form = AuthenticationForm()

    return render(
        request,
        'accounts/consumer_login.html',
        {'form': form}
    )


@login_required
@require_POST
def consumer_logout(request):
    account = AccountProfile.objects.filter(
        user=request.user,
        role='consumer'
    ).first()

    if not account:
        return redirect('home')

    logout(request)
    return redirect('home')
