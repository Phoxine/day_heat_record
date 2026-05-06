from django import forms

from .models import MealEntry, UserProfile


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["name", "height_cm", "weight_kg", "age"]
        labels = {
            "name": "名字",
            "height_cm": "身高（公分）",
            "weight_kg": "體重（公斤）",
            "age": "年齡",
        }

    def clean_name(self):
        name = self.cleaned_data["name"].strip()
        if not name:
            raise forms.ValidationError("請輸入名字。")
        return name

    def clean_height_cm(self):
        height_cm = self.cleaned_data["height_cm"]
        if height_cm <= 0:
            raise forms.ValidationError("身高必須大於 0。")
        return height_cm

    def clean_weight_kg(self):
        weight_kg = self.cleaned_data["weight_kg"]
        if weight_kg <= 0:
            raise forms.ValidationError("體重必須大於 0。")
        return weight_kg

    def clean_age(self):
        age = self.cleaned_data["age"]
        if age <= 0:
            raise forms.ValidationError("年齡必須大於 0。")
        return age


class MealEntryForm(forms.ModelForm):
    class Meta:
        model = MealEntry
        fields = ["meal_type", "food_name", "calories"]
        labels = {
            "meal_type": "餐別",
            "food_name": "食物名稱",
            "calories": "熱量（大卡）",
        }

    def clean_food_name(self):
        food_name = self.cleaned_data["food_name"].strip()
        if not food_name:
            raise forms.ValidationError("請輸入食物名稱。")
        return food_name

    def clean_calories(self):
        calories = self.cleaned_data["calories"]
        if calories <= 0:
            raise forms.ValidationError("熱量必須大於 0。")
        return calories
