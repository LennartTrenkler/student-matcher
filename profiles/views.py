import csv

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.conf import settings

from .forms import StudentProfileForm, TIME_SLOT_CHOICES
from .models import StudentProfile


def student_profile_create(request):
    if request.method == "POST":
        form = StudentProfileForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("profile_thanks")
    else:
        form = StudentProfileForm()

    return render(request, "profiles/student_profile_form.html", {"form": form})


def profile_thanks(request):
    return render(request, "profiles/thanks.html")


# ---------- teacher auth ----------

def teacher_login(request):
    error = None
    if request.method == "POST":
        password = request.POST.get("password", "")
        if password == settings.TEACHER_PASSWORD:
            request.session["teacher_ok"] = True
            return redirect("teacher_tools")
        else:
            error = "Wrong password."
    return render(request, "profiles/teacher_login.html", {"error": error})


def _require_teacher(request):
    if not request.session.get("teacher_ok"):
        return False
    return True


def teacher_tools(request):
    if not _require_teacher(request):
        return redirect("teacher_login")
    return render(request, "profiles/teacher_tools.html")


# ---------- CSV export and clear (protected) ----------

def export_profiles_csv(request):
    if not _require_teacher(request):
        return redirect("teacher_login")

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="student_profiles.csv"'

    writer = csv.writer(response)

    header = [
        "Name",
        "Mon morning (UTC)",
        "Mon afternoon (UTC)",
        "Mon evening (UTC)",
        "Tue morning (UTC)",
        "Tue afternoon (UTC)",
        "Tue evening (UTC)",
        "Wed morning (UTC)",
        "Wed afternoon (UTC)",
        "Wed evening (UTC)",
        "Thu morning (UTC)",
        "Thu afternoon (UTC)",
        "Thu evening (UTC)",
        "Fri morning (UTC)",
        "Fri afternoon (UTC)",
        "Fri evening (UTC)",
        "Sat morning (UTC)",
        "Sat afternoon (UTC)",
        "Sat evening (UTC)",
        "Sun morning (UTC)",
        "Sun afternoon (UTC)",
        "Sun evening (UTC)",
        "Commitment level",
        "Educational background",
        "Professional background",
        "Age",
        "Sex",
        "Experience level",
        "Lead/support preference",
    ]
    writer.writerow(header)

    label_map = dict(TIME_SLOT_CHOICES)

    def has_slot(text, code):
        if not text:
            return ""
        label = label_map[code]
        return "1" if label in text else ""

    for p in StudentProfile.objects.all().order_by("name"):
        row = [
            p.name,
            has_slot(p.availability_monday, "morning"),
            has_slot(p.availability_monday, "afternoon"),
            has_slot(p.availability_monday, "evening"),
            has_slot(p.availability_tuesday, "morning"),
            has_slot(p.availability_tuesday, "afternoon"),
            has_slot(p.availability_tuesday, "evening"),
            has_slot(p.availability_wednesday, "morning"),
            has_slot(p.availability_wednesday, "afternoon"),
            has_slot(p.availability_wednesday, "evening"),
            has_slot(p.availability_thursday, "morning"),
            has_slot(p.availability_thursday, "afternoon"),
            has_slot(p.availability_thursday, "evening"),
            has_slot(p.availability_friday, "morning"),
            has_slot(p.availability_friday, "afternoon"),
            has_slot(p.availability_friday, "evening"),
            has_slot(p.availability_saturday, "morning"),
            has_slot(p.availability_saturday, "afternoon"),
            has_slot(p.availability_saturday, "evening"),
            has_slot(p.availability_sunday, "morning"),
            has_slot(p.availability_sunday, "afternoon"),
            has_slot(p.availability_sunday, "evening"),
            p.commitment,
            p.educational_background,
            p.professional_background,
            p.age,
            p.sex,
            p.experience_level,
            p.lead_preference,
        ]
        writer.writerow(row)

    return response


def clear_profiles(request):
    if not _require_teacher(request):
        return redirect("teacher_login")

    if request.method == "POST":
        StudentProfile.objects.all().delete()
        return redirect("teacher_tools")

    # safety: GET just shows a confirmation
    return render(request, "profiles/confirm_clear.html")
