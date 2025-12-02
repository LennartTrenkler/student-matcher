from django.db import models

# Create your models here.
from django.db import models

class StudentProfile(models.Model):
    # Identification
    name = models.CharField(max_length=200)

    # Availability: multiple time ranges per day
    # Store as text for now → easier to implement, flexible for future changes
    availability_monday = models.TextField(blank=True)
    availability_tuesday = models.TextField(blank=True)
    availability_wednesday = models.TextField(blank=True)
    availability_thursday = models.TextField(blank=True)
    availability_friday = models.TextField(blank=True)
    availability_saturday = models.TextField(blank=True)
    availability_sunday = models.TextField(blank=True)

    # Commitment level
    commitment = models.CharField(
        max_length=20,
        choices=[
            ("minimal", "Minimal"),
            ("regular", "Regular"),
            ("high", "High"),
        ]
    )

    # Background
    educational_background = models.CharField(max_length=200, blank=True)
    professional_background = models.CharField(max_length=200, blank=True)

    # Heterogeneous criteria
    age = models.IntegerField(null=True, blank=True)
    sex = models.CharField(
        max_length=20,
        choices=[
            ("male", "Male"),
            ("female", "Female"),
            ("other", "Other"),
        ],
        blank=True
    )

    experience_level = models.CharField(
        max_length=20,
        choices=[
            ("beginner", "Beginner"),
            ("intermediate", "Intermediate"),
            ("advanced", "Advanced"),
        ],
        blank=True
    )

    lead_preference = models.CharField(
        max_length=20,
        choices=[
            ("lead", "Lead"),
            ("support", "Support")
        ],
        blank=True
    )

    def __str__(self):
        return self.name
