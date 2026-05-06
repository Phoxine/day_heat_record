from django.test import TestCase
from django.urls import reverse

from calories.models import UserProfile


class ProfileViewTests(TestCase):
    def test_home_redirects_to_profile_without_profile(self):
        response = self.client.get(reverse("calories:home"))
        self.assertRedirects(response, reverse("calories:profile"))

    def test_create_profile_redirects_to_today_record(self):
        response = self.client.post(
            reverse("calories:profile"),
            data={"name": "小明", "height_cm": 170, "weight_kg": "65.0", "age": 30},
        )
        self.assertEqual(UserProfile.objects.count(), 1)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/records/", response["Location"])
