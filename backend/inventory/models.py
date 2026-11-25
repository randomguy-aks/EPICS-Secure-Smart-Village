
from django.db import models


class Inventory(models.Model):

    product = models.OneToOneField(
        'products.Product',
        on_delete=models.CASCADE,
        related_name='inventory'
    )

    quantity = models.PositiveIntegerField(default=0)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"
