from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Sum


class UserProfile(models.Model):
    name = models.CharField("名字", max_length=80)
    height_cm = models.PositiveIntegerField("身高（公分）")
    weight_kg = models.DecimalField(
        "體重（公斤）",
        max_digits=5,
        decimal_places=1,
        validators=[MinValueValidator(Decimal("0.1"))],
    )
    age = models.PositiveIntegerField("年齡")
    created_at = models.DateTimeField("建立時間", auto_now_add=True)
    updated_at = models.DateTimeField("更新時間", auto_now=True)

    class Meta:
        verbose_name = "使用者資料"
        verbose_name_plural = "使用者資料"

    def clean(self):
        super().clean()
        self.name = self.name.strip() if self.name else ""
        if not self.name:
            raise ValidationError({"name": "請輸入名字。"})
        if self.height_cm <= 0:
            raise ValidationError({"height_cm": "身高必須大於 0。"})
        if self.weight_kg <= 0:
            raise ValidationError({"weight_kg": "體重必須大於 0。"})
        if self.age <= 0:
            raise ValidationError({"age": "年齡必須大於 0。"})
        if not self.pk and UserProfile.objects.exists():
            raise ValidationError("MVP 目前只支援一位使用者。")

    def __str__(self):
        return self.name


class DailyRecord(models.Model):
    profile = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name="daily_records",
        verbose_name="使用者資料",
    )
    date = models.DateField("日期")
    created_at = models.DateTimeField("建立時間", auto_now_add=True)
    updated_at = models.DateTimeField("更新時間", auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["profile", "date"], name="unique_profile_date")
        ]
        ordering = ["-date"]
        verbose_name = "每日記錄"
        verbose_name_plural = "每日記錄"

    def meal_total(self, meal_type):
        total = self.entries.filter(meal_type=meal_type).aggregate(total=Sum("calories"))["total"]
        return total or 0

    @property
    def total_calories(self):
        total = self.entries.aggregate(total=Sum("calories"))["total"]
        return total or 0

    def __str__(self):
        return f"{self.profile.name} - {self.date}"


class MealEntry(models.Model):
    BREAKFAST = "breakfast"
    LUNCH = "lunch"
    DINNER = "dinner"

    MEAL_CHOICES = [
        (BREAKFAST, "早餐"),
        (LUNCH, "午餐"),
        (DINNER, "晚餐"),
    ]

    daily_record = models.ForeignKey(
        DailyRecord,
        on_delete=models.CASCADE,
        related_name="entries",
        verbose_name="每日記錄",
    )
    meal_type = models.CharField("餐別", max_length=20, choices=MEAL_CHOICES)
    food_name = models.CharField("食物名稱", max_length=120)
    calories = models.PositiveIntegerField("熱量", validators=[MinValueValidator(1)])
    created_at = models.DateTimeField("建立時間", auto_now_add=True)
    updated_at = models.DateTimeField("更新時間", auto_now=True)

    class Meta:
        ordering = ["created_at", "id"]
        verbose_name = "食物項目"
        verbose_name_plural = "食物項目"

    def clean(self):
        super().clean()
        self.food_name = self.food_name.strip() if self.food_name else ""
        if not self.food_name:
            raise ValidationError({"food_name": "請輸入食物名稱。"})
        if self.calories <= 0:
            raise ValidationError({"calories": "熱量必須大於 0。"})
        valid_meals = {choice[0] for choice in self.MEAL_CHOICES}
        if self.meal_type not in valid_meals:
            raise ValidationError({"meal_type": "請選擇有效的餐別。"})

    @property
    def meal_label(self):
        return dict(self.MEAL_CHOICES).get(self.meal_type, self.meal_type)

    def __str__(self):
        return f"{self.meal_label} - {self.food_name} ({self.calories} 大卡)"
