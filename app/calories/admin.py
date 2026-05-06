from django.contrib import admin

from .models import DailyRecord, MealEntry, UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("name", "height_cm", "weight_kg", "age", "updated_at")


class MealEntryInline(admin.TabularInline):
    model = MealEntry
    extra = 0


@admin.register(DailyRecord)
class DailyRecordAdmin(admin.ModelAdmin):
    list_display = ("profile", "date", "total_calories")
    list_filter = ("date",)
    inlines = [MealEntryInline]


@admin.register(MealEntry)
class MealEntryAdmin(admin.ModelAdmin):
    list_display = ("food_name", "meal_type", "calories", "daily_record")
    list_filter = ("meal_type", "daily_record__date")
