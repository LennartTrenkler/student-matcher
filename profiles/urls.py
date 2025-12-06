from django.urls import path
from . import views

urlpatterns = [
    path("teacher-login/", views.teacher_login, name="teacher_login"),
    path("teacher-tools/", views.teacher_tools, name="teacher_tools"),
    path("download-csv/", views.export_profiles_csv, name="export_profiles_csv"),
    path("clear-profiles/", views.clear_profiles, name="clear_profiles"),

    # main student form
    path("", views.student_profile_create, name="student_profile_create"),
    path("thanks/", views.profile_thanks, name="profile_thanks"),
]
