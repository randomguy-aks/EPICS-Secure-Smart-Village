
from django.db import models
from django.contrib.auth.models import User


class SellerProfile(models.Model):

    SELLER_TYPES = [
        ('individual', 'Individual Seller'),
        ('organization', 'Organization'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='seller_profile'
    )

    seller_type = models.CharField(
        max_length=20,
        choices=SELLER_TYPES,
        default='individual'
    )

    business_name = models.CharField(max_length=150)

    description = models.TextField(blank=True)

    operating_location = models.CharField(max_length=255)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.business_name
