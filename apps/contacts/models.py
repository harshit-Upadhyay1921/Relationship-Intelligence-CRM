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

    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class SummaryStatus(models.TextChoices):
        NOT_GENERATED = "NOT_GENERATED", "Not Generated"
        READY = "READY", "Ready"
        STALE = "STALE", "Stale"
        GENERATING = "GENERATING", "Generating"

    ai_summary = models.TextField(blank=True, null=True)

    summary_status = models.CharField(
        max_length=20,
        choices=SummaryStatus.choices,
        default=SummaryStatus.NOT_GENERATED,
    )

    summary_generated_at = models.DateTimeField(
        null=True,
        blank=True,
    )
    
    # Persisted in the database because Celery recalculates it periodically.
    # This replaces the earlier computed @property for better performance.
    relationship_score = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    @property
    def last_interaction_date(self):
        return RelationshipScoringService.get_last_interaction(self)

    # earlier needed but not now since we are persisting the score in the contact model as it will be calculated and updated every night by a scheduled task. So, we don't need to calculate it on the fly anymore.
    # @property
    # def relationship_score(self):
    #     return RelationshipScoringService.calculate_relationship_score(
    #         self.last_interaction_date
    #     )

    @property
    def needs_follow_up(self):
        return self.relationship_score < 50
    
