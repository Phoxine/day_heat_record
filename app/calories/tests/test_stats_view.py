from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from calories.models import UserProfile


class StatsViewTests(TestCase):
    def test_redirects_to_profile_without_profile(self):
        response = self.client.get(reverse("calories:stats"))
        self.assertRedirects(response, reverse("calories:profile"))

    def test_empty_state_with_profile(self):
        UserProfile.objects.create(name="小明", height_cm=170, weight_kg=Decimal("65.0"), age=30)
        response = self.client.get(reverse("calories:stats"))
        self.assertContains(response, "還沒有統計資料")
        self.assertContains(response, "回到今日記錄")
