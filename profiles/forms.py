from django import forms
from .models import StudentProfile, Task


# Time slots (unchanged)
TIME_SLOT_CHOICES = [
    ("morning", "Morning 06:00-12:00 (UTC)"),
    ("afternoon", "Afternoon 12:00-18:00 (UTC)"),
    ("evening", "Evening 18:00-24:00 (UTC)"),
]

# NEW: educational background options
EDUCATION_CHOICES = [
    ("none_yet", "No degree yet / Bachelor in progress"),
    ("bachelor_business", "Bachelor – Business / Management / Economics"),
    ("bachelor_cs", "Bachelor – Computer Science / IT"),
    ("bachelor_engineering", "Bachelor – Engineering"),
    ("bachelor_social", "Bachelor – Social Sciences / Humanities"),
    ("master_business", "Master – Business / Management / Economics"),
    ("master_other", "Master – other field"),
    ("other", "Other / different background"),
]

# NEW: professional background options
PROFESSIONAL_CHOICES = [
    ("none", "No professional experience yet"),
    ("internship", "Internships only"),
    ("working_student", "Working student / part-time job"),
    ("industry_business", "Industry – Business / Management"),
    ("industry_it", "Industry – IT / Software / Data"),
    ("industry_other", "Industry – other field"),
]


def _join_slots(codes):
    """Convert selected slot codes into a readable string."""
    label_map = dict(TIME_SLOT_CHOICES)
    labels = [label_map[c] for c in codes]
    return ", ".join(labels)


class StudentProfileForm(forms.ModelForm):
    # Availability fields as multi-select checkboxes
    availability_monday = forms.MultipleChoiceField(
        required=False,
        choices=TIME_SLOT_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        label="Monday availability (UTC)",
    )
    availability_tuesday = forms.MultipleChoiceField(
        required=False,
        choices=TIME_SLOT_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        label="Tuesday availability (UTC)",
    )
    availability_wednesday = forms.MultipleChoiceField(
        required=False,
        choices=TIME_SLOT_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        label="Wednesday availability (UTC)",
    )
    availability_thursday = forms.MultipleChoiceField(
        required=False,
        choices=TIME_SLOT_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        label="Thursday availability (UTC)",
    )
    availability_friday = forms.MultipleChoiceField(
        required=False,
        choices=TIME_SLOT_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        label="Friday availability (UTC)",
    )
    availability_saturday = forms.MultipleChoiceField(
        required=False,
        choices=TIME_SLOT_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        label="Saturday availability (UTC)",
    )
    availability_sunday = forms.MultipleChoiceField(
        required=False,
        choices=TIME_SLOT_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        label="Sunday availability (UTC)",
    )

    # NEW: override age field – numbers only, 0–99
    age = forms.IntegerField(
        required=False,
        min_value=0,
        max_value=99,
        label="Age",
        widget=forms.NumberInput(attrs={"min": 0, "max": 99}),
    )

    # NEW: dropdown for educational background
    educational_background = forms.ChoiceField(
        required=False,
        choices=EDUCATION_CHOICES,
        label="Educational background",
    )

    # NEW: dropdown for professional background
    professional_background = forms.ChoiceField(
        required=False,
        choices=PROFESSIONAL_CHOICES,
        label="Professional background",
    )

    # Tasks from admin, multi-select
    preferred_tasks = forms.ModelMultipleChoiceField(
        queryset=Task.objects.filter(active=True),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Preferred tasks",
    )

    class Meta:
        model = StudentProfile
        fields = [
            "name",
            "availability_monday",
            "availability_tuesday",
            "availability_wednesday",
            "availability_thursday",
            "availability_friday",
            "availability_saturday",
            "availability_sunday",
            "commitment",
            "educational_background",
            "professional_background",
            "age",
            "sex",
            "experience_level",
            "lead_preference",
            "preferred_tasks",
        ]

    # Clean methods to store availability as readable strings
    def clean_availability_monday(self):
        return _join_slots(self.cleaned_data["availability_monday"])

    def clean_availability_tuesday(self):
        return _join_slots(self.cleaned_data["availability_tuesday"])

    def clean_availability_wednesday(self):
        return _join_slots(self.cleaned_data["availability_wednesday"])

    def clean_availability_thursday(self):
        return _join_slots(self.cleaned_data["availability_thursday"])

    def clean_availability_friday(self):
        return _join_slots(self.cleaned_data["availability_friday"])

    def clean_availability_saturday(self):
        return _join_slots(self.cleaned_data["availability_saturday"])

    def clean_availability_sunday(self):
        return _join_slots(self.cleaned_data["availability_sunday"])

    # Extra safety: age validation (two digits)
    def clean_age(self):
        age = self.cleaned_data.get("age")
        if age is None:
            return age
        if age < 0 or age > 99:
            raise forms.ValidationError("Please enter an age between 0 and 99.")
        return age
