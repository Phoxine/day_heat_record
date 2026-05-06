from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from calories.models import DailyRecord, MealEntry, UserProfile


class DateRecordTests(TestCase):
    def setUp(self):
        self.profile = UserProfile.objects.create(
            name="小明", height_cm=170, weight_kg=Decimal("65.0"), age=30
        )

    def test_records_are_isolated_by_date(self):
        self.client.post(
            reverse("calories:add_entry", args=["2026-05-05"]),
            data={"meal_type": MealEntry.LUNCH, "food_name": "飯糰", "calories": 300},
        )
        self.client.post(
            reverse("calories:add_entry", args=["2026-05-06"]),
            data={"meal_type": MealEntry.LUNCH, "food_name": "便當", "calories": 700},
        )

        yesterday = DailyRecord.objects.get(profile=self.profile, date="2026-05-05")
        today = DailyRecord.objects.get(profile=self.profile, date="2026-05-06")
        self.assertEqual(yesterday.total_calories, 300)
        self.assertEqual(today.total_calories, 700)

        response = self.client.get(reverse("calories:record_detail", args=["2026-05-05"]))
        self.assertContains(response, "飯糰")
        self.assertNotContains(response, "便當")
