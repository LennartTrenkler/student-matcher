from django.contrib import admin
from .models import StudentProfile, Task


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ("name", "commitment", "experience_level")


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("name", "active")
    list_filter = ("active",)
    search_fields = ("name",)
