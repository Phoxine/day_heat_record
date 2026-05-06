from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from calories.models import DailyRecord, MealEntry, UserProfile


class RecordViewTests(TestCase):
    def setUp(self):
        self.profile = UserProfile.objects.create(
            name="小明", height_cm=170, weight_kg=Decimal("65.0"), age=30
        )

    def test_add_three_meals_and_totals(self):
        date = "2026-05-06"
        url = reverse("calories:add_entry", args=[date])
        meals = [
            (MealEntry.BREAKFAST, "吐司", 250),
            (MealEntry.LUNCH, "便當", 700),
            (MealEntry.DINNER, "沙拉", 320),
        ]
        for meal_type, food_name, calories in meals:
            response = self.client.post(
                url,
                data={"meal_type": meal_type, "food_name": food_name, "calories": calories},
            )
            self.assertRedirects(response, reverse("calories:record_detail", args=[date]))

        record = DailyRecord.objects.get(profile=self.profile, date=date)
        self.assertEqual(record.meal_total(MealEntry.BREAKFAST), 250)
        self.assertEqual(record.meal_total(MealEntry.LUNCH), 700)
        self.assertEqual(record.meal_total(MealEntry.DINNER), 320)
        self.assertEqual(record.total_calories, 1270)

        response = self.client.get(reverse("calories:record_detail", args=[date]))
        self.assertContains(response, "1270 大卡")
