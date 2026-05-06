from django.urls import path

from . import views


app_name = "calories"

urlpatterns = [
    path("", views.home, name="home"),
    path("profile/", views.profile, name="profile"),
    path("records/<str:date>/", views.record_detail, name="record_detail"),
    path("records/<str:date>/entries/", views.add_entry, name="add_entry"),
    path("entries/<int:entry_id>/edit/", views.edit_entry, name="edit_entry"),
    path("entries/<int:entry_id>/delete/", views.delete_entry, name="delete_entry"),
    path("stats/", views.stats, name="stats"),
]
