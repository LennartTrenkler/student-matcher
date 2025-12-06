import csv

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import StudentProfileForm, TIME_SLOT_CHOICES
from .models import StudentProfile


def student_profile_create(request):
    """Main student input form."""
    if request.method == "POST":
        form = StudentProfileForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("profile_thanks")
    else:
        form = StudentProfileForm()

    is_teacher = request.session.get("teacher_ok", False)

    return render(
        request,
        "profiles/student_profile_form.html",
        {
            "form": form,
            "is_teacher": is_teacher,
        },
    )


def profile_thanks(request):
    """Simple thank-you page after submission."""
    is_teacher = request.session.get("teacher_ok", False)
    return render(request, "profiles/thanks.html", {"is_teacher": is_teacher})


# ---------------------------------------------------------------------
# Teacher authentication
# ---------------------------------------------------------------------


def teacher_login(request):
    """Password-based login for teacher actions."""
    error = None

    if request.method == "POST":
        password = request.POST.get("password", "")
        if password == settings.TEACHER_PASSWORD:
            request.session["teacher_ok"] = True
            # redirect back to form by default
            next_url = request.GET.get("next") or "student_profile_create"
            return redirect(next_url)
        else:
            error = "Wrong password."

    return render(request, "profiles/teacher_login.html", {"error": error})


def teacher_tools(request):
    """
    Legacy view; currently just redirects an authenticated teacher
    back to the main form.
    """
    if not request.session.get("teacher_ok"):
        return redirect("teacher_login")
    return redirect("student_profile_create")


# ---------------------------------------------------------------------
# CSV export (teacher only)
# ---------------------------------------------------------------------


def export_profiles_csv(request):
    """Download all student profiles as a CSV file (teacher only)."""
    if not request.session.get("teacher_ok"):
        # remember where to come back to after login
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
        "Preferred tasks",
    ]
    writer.writerow(header)

    label_map = dict(TIME_SLOT_CHOICES)

    def has_slot(text, code):
        """Return '1' if the given slot label is present in the text, else ''."""
        if not text:
            return ""
        label = label_map[code]
        return "1" if label in text else ""

    for p in StudentProfile.objects.all().order_by("name"):
        preferred_tasks = ", ".join(t.name for t in p.preferred_tasks.all())

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
            preferred_tasks,
        ]
        writer.writerow(row)

    return response


# ---------------------------------------------------------------------
# Clear all profiles (teacher only, with confirmation)
# ---------------------------------------------------------------------


def clear_profiles(request):
    """Delete all StudentProfile entries (teacher only, with confirm page)."""
    if not request.session.get("teacher_ok"):
        return redirect("teacher_login")

    if request.method == "POST":
        StudentProfile.objects.all().delete()
        return redirect("student_profile_create")

    # GET → render confirmation page
    return render(request, "profiles/confirm_clear.html")
