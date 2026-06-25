from django.conf import settings
from django.db import models

from apps.companies.models import Company

from .services import RelationshipScoringService

class Contact(models.Model):

    class Status(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        DORMANT = "DORMANT", "Dormant"
        ARCHIVED = "ARCHIVED", "Archived"

    class Category(models.TextChoices):
        MENTOR = "MENTOR", "Mentor"
        FOUNDER = "FOUNDER", "Founder"
        INVESTOR = "INVESTOR", "Investor"
        RECRUITER = "RECRUITER", "Recruiter"
        COLLEAGUE = "COLLEAGUE", "Colleague"
        OTHER = "OTHER", "Other"

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="contacts"
    )

    company = models.ForeignKey(
        Company,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="contacts"
    )

    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    job_title = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE
    )

    category = models.CharField(
        max_length=20,
        choices=Category.choices,
        default=Category.OTHER
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def last_interaction_date(self):
        return RelationshipScoringService.get_last_interaction(self)

    @property
    def relationship_score(self):
        return RelationshipScoringService.calculate_relationship_score(
            self.last_interaction_date
        )

    @property
    def needs_follow_up(self):
        return RelationshipScoringService.needs_follow_up(self)
