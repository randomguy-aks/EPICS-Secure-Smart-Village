from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from accounts.models import AccountProfile
from sellers.models import SellerProfile


class SellerDashboardSecurityTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="seller_test",
            password="Strong-test-password-123"
        )
        AccountProfile.objects.create(user=self.user, role="seller")

    def test_inactive_seller_cannot_access_dashboard(self):
        SellerProfile.objects.create(
            user=self.user,
            business_name="Test Farm",
            operating_location="Village",
            is_active=False,
        )
        self.client.force_login(self.user)

        response = self.client.get(reverse("seller_dashboard"))

        self.assertRedirects(response, reverse("home"))

    def test_active_seller_can_access_dashboard(self):
        SellerProfile.objects.create(
            user=self.user,
            business_name="Test Farm",
            operating_location="Village",
            is_active=True,
        )
        self.client.force_login(self.user)

        response = self.client.get(reverse("seller_dashboard"))

        self.assertEqual(response.status_code, 200)

    def test_consumer_cannot_access_seller_dashboard(self):
        AccountProfile.objects.filter(user=self.user).update(role="consumer")
        self.client.force_login(self.user)

        response = self.client.get(reverse("seller_dashboard"))

        self.assertRedirects(response, reverse("home"))
