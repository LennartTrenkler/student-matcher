from django.db import models


class Task(models.Model):
    name = models.CharField(max_length=200)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


COMMITMENT_CHOICES = [
    ("minimal", "Minimal"),
    ("regular", "Regular"),
    ("high", "High"),
]

EXPERIENCE_CHOICES = [
    ("beginner", "Beginner"),
    ("intermediate", "Intermediate"),
    ("advanced", "Advanced"),
]

LEAD_CHOICES = [
    ("lead", "Lead"),
    ("support", "Support"),
]

SEX_CHOICES = [
    ("female", "Female"),
    ("male", "Male"),
    ("other", "Other / prefer not to say"),
]


class StudentProfile(models.Model):
    name = models.CharField(max_length=200)

    availability_monday = models.CharField(max_length=200, blank=True)
    availability_tuesday = models.CharField(max_length=200, blank=True)
    availability_wednesday = models.CharField(max_length=200, blank=True)
    availability_thursday = models.CharField(max_length=200, blank=True)
    availability_friday = models.CharField(max_length=200, blank=True)
    availability_saturday = models.CharField(max_length=200, blank=True)
    availability_sunday = models.CharField(max_length=200, blank=True)

    commitment = models.CharField(
        max_length=20, choices=COMMITMENT_CHOICES, blank=True
    )
    educational_background = models.CharField(max_length=200, blank=True)
    professional_background = models.CharField(max_length=200, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    sex = models.CharField(max_length=20, choices=SEX_CHOICES, blank=True)
    experience_level = models.CharField(
        max_length=20, choices=EXPERIENCE_CHOICES, blank=True
    )
    lead_preference = models.CharField(
        max_length=20, choices=LEAD_CHOICES, blank=True
    )

    # NEW: teacher-configurable tasks, multi-select on form
    preferred_tasks = models.ManyToManyField(Task, blank=True)

    def __str__(self):
        return self.name
