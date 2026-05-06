from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from calories.models import DailyRecord, MealEntry, UserProfile


class EntryMutationTests(TestCase):
    def setUp(self):
        self.profile = UserProfile.objects.create(
            name="小明", height_cm=170, weight_kg=Decimal("65.0"), age=30
        )
        self.record = DailyRecord.objects.create(profile=self.profile, date="2026-05-06")
        self.entry = MealEntry.objects.create(
            daily_record=self.record,
            meal_type=MealEntry.DINNER,
            food_name="晚餐",
            calories=500,
        )

    def test_edit_entry_updates_total(self):
        response = self.client.post(
            reverse("calories:edit_entry", args=[self.entry.id]),
            data={"meal_type": MealEntry.DINNER, "food_name": "雞胸", "calories": 420},
        )
        self.assertRedirects(response, reverse("calories:record_detail", args=["2026-05-06"]))
        self.entry.refresh_from_db()
        self.assertEqual(self.entry.food_name, "雞胸")
        self.assertEqual(self.record.total_calories, 420)

    def test_delete_entry_updates_total(self):
        response = self.client.post(reverse("calories:delete_entry", args=[self.entry.id]))
        self.assertRedirects(response, reverse("calories:record_detail", args=["2026-05-06"]))
        self.assertEqual(MealEntry.objects.count(), 0)
        self.assertEqual(self.record.total_calories, 0)
