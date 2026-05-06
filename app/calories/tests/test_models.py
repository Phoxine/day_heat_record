from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from calories.models import DailyRecord, MealEntry, UserProfile


class ModelValidationTests(TestCase):
    def test_profile_requires_valid_fields(self):
        profile = UserProfile(name="  ", height_cm=170, weight_kg=Decimal("65.0"), age=30)
        with self.assertRaises(ValidationError):
            profile.full_clean()

    def test_daily_record_unique_per_profile_date(self):
        profile = UserProfile.objects.create(name="小明", height_cm=170, weight_kg=Decimal("65.0"), age=30)
        DailyRecord.objects.create(profile=profile, date="2026-05-06")
        with self.assertRaises(IntegrityError):
            DailyRecord.objects.create(profile=profile, date="2026-05-06")

    def test_meal_entry_requires_food_name_and_positive_calories(self):
        profile = UserProfile.objects.create(name="小明", height_cm=170, weight_kg=Decimal("65.0"), age=30)
        record = DailyRecord.objects.create(profile=profile, date="2026-05-06")
        entry = MealEntry(
            daily_record=record,
            meal_type=MealEntry.BREAKFAST,
            food_name="",
            calories=0,
        )
        with self.assertRaises(ValidationError):
            entry.full_clean()
