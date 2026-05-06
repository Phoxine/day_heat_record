from datetime import timedelta
from decimal import Decimal

from django.test import TestCase
from django.utils import timezone

from calories.models import DailyRecord, MealEntry, UserProfile
from calories.views import calculate_statistics


class StatisticsTests(TestCase):
    def setUp(self):
        self.profile = UserProfile.objects.create(
            name="小明", height_cm=170, weight_kg=Decimal("65.0"), age=30
        )

    def add_entry(self, days_ago, meal_type, calories):
        record = DailyRecord.objects.create(
            profile=self.profile,
            date=timezone.localdate() - timedelta(days=days_ago),
        )
        return MealEntry.objects.create(
            daily_record=record,
            meal_type=meal_type,
            food_name=f"{meal_type}-{days_ago}",
            calories=calories,
        )

    def test_statistics_include_highest_day_and_primary_meal(self):
        self.add_entry(0, MealEntry.BREAKFAST, 200)
        self.add_entry(1, MealEntry.LUNCH, 800)
        self.add_entry(2, MealEntry.LUNCH, 600)

        stats = calculate_statistics(self.profile, 7)

        self.assertEqual(stats["total_calories"], 1600)
        self.assertEqual(stats["recorded_days"], 3)
        self.assertEqual(stats["average_daily"], 533)
        self.assertEqual(stats["primary_meal"]["label"], "午餐")
        self.assertEqual(stats["highest_day"]["total"], 800)
