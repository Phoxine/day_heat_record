from django.test import TestCase

from calories.forms import MealEntryForm, UserProfileForm
from calories.models import MealEntry


class FormValidationTests(TestCase):
    def test_profile_form_rejects_invalid_values(self):
        form = UserProfileForm(
            data={"name": "", "height_cm": 0, "weight_kg": 0, "age": 0}
        )
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)
        self.assertIn("height_cm", form.errors)
        self.assertIn("weight_kg", form.errors)
        self.assertIn("age", form.errors)

    def test_meal_entry_form_rejects_invalid_values(self):
        form = MealEntryForm(
            data={"meal_type": MealEntry.BREAKFAST, "food_name": "", "calories": 0}
        )
        self.assertFalse(form.is_valid())
        self.assertIn("food_name", form.errors)
        self.assertIn("calories", form.errors)
