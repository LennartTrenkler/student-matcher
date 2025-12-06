from django.urls import path
from . import views

urlpatterns = [
    path("", views.student_profile_create, name="student_profile_form"),
    path("thanks/", views.profile_thanks, name="profile_thanks"),
]
