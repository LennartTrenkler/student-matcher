from django import forms
from .models import StudentProfile


TIME_SLOT_CHOICES = [
    ("morning", "Morning 06:00-12:00 (UTC)"),
    ("afternoon", "Afternoon 12:00-18:00 (UTC)"),
    ("evening", "Evening 18:00-24:00 (UTC)"),
]


def _join_slots(codes):
    """
    Convert list of selected slot codes into a readable string
    using the labels defined in TIME_SLOT_CHOICES.
    """
    label_map = dict(TIME_SLOT_CHOICES)
    labels = [label_map[c] for c in codes]
    return ", ".join(labels)


class StudentProfileForm(forms.ModelForm):
    # override availability fields with multi-select checkboxes
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
        ]

    # convert selected codes → readable string for storage

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
