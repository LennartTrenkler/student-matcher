from django.urls import path
from . import views

urlpatterns = [
    path("", views.student_profile_create, name="student_profile_form"),
    path("thanks/", views.profile_thanks, name="profile_thanks"),

    # teacher area
    path("teacher/login/", views.teacher_login, name="teacher_login"),
    path("teacher/", views.teacher_tools, name="teacher_tools"),
    path("teacher/export/", views.export_profiles_csv, name="export_profiles_csv"),
    path("teacher/clear/", views.clear_profiles, name="clear_profiles"),
]
