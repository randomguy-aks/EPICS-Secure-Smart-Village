from django.contrib.auth.models import User
from django.test import TestCase

from products.forms import ProductForm
from products.models import Category


class ProductFormSecurityTests(TestCase):
    def setUp(self):
        self.active_category = Category.objects.create(
            name="Active category",
            is_active=True,
        )
        self.inactive_category = Category.objects.create(
            name="Inactive category",
            is_active=False,
        )

    def test_inactive_category_is_not_available_for_product_form(self):
        form = ProductForm()

        self.assertQuerySetEqual(
            form.fields["category"].queryset,
            [self.active_category],
        )

    def test_inactive_category_submission_is_rejected(self):
        form = ProductForm(data={
            "category": self.inactive_category.pk,
            "name": "Test produce",
            "description": "Fresh produce",
            "price": "10.00",
            "unit": "kg",
            "quantity": "5",
        })

        self.assertFalse(form.is_valid())
        self.assertIn("category", form.errors)

    def test_zero_or_negative_price_is_rejected(self):
        for price in ("0", "-1"):
            form = ProductForm(data={
                "category": self.active_category.pk,
                "name": "Test produce",
                "description": "Fresh produce",
                "price": price,
                "unit": "kg",
                "quantity": "5",
            })

            self.assertFalse(form.is_valid())
            self.assertIn("price", form.errors)
