from datetime import timedelta

from django.contrib import messages
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.dateparse import parse_date

from .forms import MealEntryForm, UserProfileForm
from .models import DailyRecord, MealEntry, UserProfile


MEAL_ORDER = [MealEntry.BREAKFAST, MealEntry.LUNCH, MealEntry.DINNER]


def get_profile():
    return UserProfile.objects.first()


def today():
    return timezone.localdate()


def parse_record_date(date_text):
    parsed = parse_date(date_text)
    return parsed or today()


def home(request):
    profile = get_profile()
    if profile:
        return redirect("calories:record_detail", date=today().isoformat())
    return redirect("calories:profile")


def profile(request):
    profile_obj = get_profile()
    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=profile_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "個人資料已儲存。")
            return redirect("calories:record_detail", date=today().isoformat())
        messages.error(request, "請修正表單中的錯誤。")
    else:
        form = UserProfileForm(instance=profile_obj)

    return render(request, "calories/profile_form.html", {"form": form, "profile": profile_obj})


def get_record_for_date(profile_obj, record_date):
    return DailyRecord.objects.get_or_create(profile=profile_obj, date=record_date)[0]


def record_context(profile_obj, record_date, entry_form=None, edit_entry_id=None, edit_form=None):
    record = get_record_for_date(profile_obj, record_date)
    entries_by_meal = {}
    meal_totals = {}
    for meal_type, meal_label in MealEntry.MEAL_CHOICES:
        entries = list(record.entries.filter(meal_type=meal_type))
        entries_by_meal[meal_type] = {
            "label": meal_label,
            "entries": entries,
            "total": record.meal_total(meal_type),
        }
        meal_totals[meal_type] = entries_by_meal[meal_type]["total"]

    return {
        "profile": profile_obj,
        "record": record,
        "record_date": record_date,
        "previous_date": (record_date - timedelta(days=1)).isoformat(),
        "next_date": (record_date + timedelta(days=1)).isoformat(),
        "entry_form": entry_form or MealEntryForm(),
        "entries_by_meal": entries_by_meal,
        "meal_order": MEAL_ORDER,
        "meal_totals": meal_totals,
        "total_calories": record.total_calories,
        "edit_entry_id": edit_entry_id,
        "edit_form": edit_form,
    }


def record_detail(request, date):
    profile_obj = get_profile()
    if not profile_obj:
        messages.info(request, "請先建立個人資料。")
        return redirect("calories:profile")
    record_date = parse_record_date(date)
    return render(request, "calories/record_detail.html", record_context(profile_obj, record_date))


def add_entry(request, date):
    profile_obj = get_profile()
    if not profile_obj:
        return redirect("calories:profile")
    record_date = parse_record_date(date)
    record = get_record_for_date(profile_obj, record_date)
    form = MealEntryForm(request.POST)
    if form.is_valid():
        entry = form.save(commit=False)
        entry.daily_record = record
        entry.save()
        messages.success(request, "餐點已新增。")
        return redirect("calories:record_detail", date=record_date.isoformat())
    messages.error(request, "請修正餐點資料。")
    return render(request, "calories/record_detail.html", record_context(profile_obj, record_date, entry_form=form))


def edit_entry(request, entry_id):
    entry = get_object_or_404(MealEntry, id=entry_id)
    record_date = entry.daily_record.date
    profile_obj = entry.daily_record.profile
    if request.method == "POST":
        data = request.POST.copy()
        data.setdefault("meal_type", entry.meal_type)
        form = MealEntryForm(data, instance=entry)
        if form.is_valid():
            form.save()
            messages.success(request, "餐點已更新。")
            return redirect("calories:record_detail", date=record_date.isoformat())
        messages.error(request, "請修正餐點資料。")
        return render(
            request,
            "calories/record_detail.html",
            record_context(profile_obj, record_date, edit_entry_id=entry.id, edit_form=form),
        )
    return redirect("calories:record_detail", date=record_date.isoformat())


def delete_entry(request, entry_id):
    entry = get_object_or_404(MealEntry, id=entry_id)
    record_date = entry.daily_record.date
    if request.method == "POST":
        entry.delete()
        messages.success(request, "餐點已刪除。")
    return redirect("calories:record_detail", date=record_date.isoformat())


def calculate_statistics(profile_obj, period):
    end_date = today()
    start_date = end_date - timedelta(days=period - 1)
    records = DailyRecord.objects.filter(profile=profile_obj, date__range=(start_date, end_date))
    entries = MealEntry.objects.filter(daily_record__in=records)

    total_calories = entries.aggregate(total=Sum("calories"))["total"] or 0
    daily_totals = list(
        entries.values("daily_record__date")
        .annotate(total=Sum("calories"))
        .order_by("-daily_record__date")
    )
    recorded_days = len(daily_totals)
    average_daily = round(total_calories / recorded_days) if recorded_days else 0

    meal_totals = {}
    for meal_type, meal_label in MealEntry.MEAL_CHOICES:
        meal_total = entries.filter(meal_type=meal_type).aggregate(total=Sum("calories"))["total"] or 0
        meal_totals[meal_type] = {
            "label": meal_label,
            "total": meal_total,
            "percent": round((meal_total / total_calories) * 100) if total_calories else 0,
        }

    highest_day = max(daily_totals, key=lambda item: item["total"], default=None)
    primary_meal = max(meal_totals.values(), key=lambda item: item["total"], default=None)
    if primary_meal and primary_meal["total"] == 0:
        primary_meal = None

    return {
        "period": period,
        "start_date": start_date,
        "end_date": end_date,
        "total_calories": total_calories,
        "recorded_days": recorded_days,
        "average_daily": average_daily,
        "meal_totals": meal_totals,
        "daily_totals": daily_totals,
        "highest_day": highest_day,
        "primary_meal": primary_meal,
    }


def stats(request):
    profile_obj = get_profile()
    if not profile_obj:
        messages.info(request, "請先建立個人資料。")
        return redirect("calories:profile")

    try:
        period = int(request.GET.get("period", "7"))
    except ValueError:
        period = 7
    if period not in (7, 30):
        period = 7

    statistics = calculate_statistics(profile_obj, period)
    return render(request, "calories/stats.html", {"profile": profile_obj, "statistics": statistics})
