# Generated manually for the Spec Kit MVP.

import django.core.validators
from decimal import Decimal
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="UserProfile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=80, verbose_name="名字")),
                ("height_cm", models.PositiveIntegerField(verbose_name="身高（公分）")),
                (
                    "weight_kg",
                    models.DecimalField(
                        decimal_places=1,
                        max_digits=5,
                        validators=[django.core.validators.MinValueValidator(Decimal("0.1"))],
                        verbose_name="體重（公斤）",
                    ),
                ),
                ("age", models.PositiveIntegerField(verbose_name="年齡")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="建立時間")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="更新時間")),
            ],
            options={
                "verbose_name": "使用者資料",
                "verbose_name_plural": "使用者資料",
            },
        ),
        migrations.CreateModel(
            name="DailyRecord",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("date", models.DateField(verbose_name="日期")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="建立時間")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="更新時間")),
                (
                    "profile",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="daily_records",
                        to="calories.userprofile",
                        verbose_name="使用者資料",
                    ),
                ),
            ],
            options={
                "verbose_name": "每日記錄",
                "verbose_name_plural": "每日記錄",
                "ordering": ["-date"],
            },
        ),
        migrations.CreateModel(
            name="MealEntry",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "meal_type",
                    models.CharField(
                        choices=[("breakfast", "早餐"), ("lunch", "午餐"), ("dinner", "晚餐")],
                        max_length=20,
                        verbose_name="餐別",
                    ),
                ),
                ("food_name", models.CharField(max_length=120, verbose_name="食物名稱")),
                (
                    "calories",
                    models.PositiveIntegerField(
                        validators=[django.core.validators.MinValueValidator(1)],
                        verbose_name="熱量",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="建立時間")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="更新時間")),
                (
                    "daily_record",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="entries",
                        to="calories.dailyrecord",
                        verbose_name="每日記錄",
                    ),
                ),
            ],
            options={
                "verbose_name": "食物項目",
                "verbose_name_plural": "食物項目",
                "ordering": ["created_at", "id"],
            },
        ),
        migrations.AddConstraint(
            model_name="dailyrecord",
            constraint=models.UniqueConstraint(fields=("profile", "date"), name="unique_profile_date"),
        ),
    ]
