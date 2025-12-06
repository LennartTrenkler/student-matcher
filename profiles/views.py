from django.shortcuts import render, redirect

from .forms import StudentProfileForm


def student_profile_create(request):
    """Main student input form."""
    if request.method == "POST":
        form = StudentProfileForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("profile_thanks")
    else:
        form = StudentProfileForm()

    return render(
        request,
        "profiles/student_profile_form.html",
        {"form": form},
    )


def profile_thanks(request):
    """Simple thank-you page after submission."""
    return render(request, "profiles/thanks.html")
