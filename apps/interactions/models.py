from django.db import models

from apps.contacts.models import Contact


class Interaction(models.Model):

    class InteractionType(models.TextChoices):
        CALL = "CALL", "Call"
        MEETING = "MEETING", "Meeting"
        EMAIL = "EMAIL", "Email"
        LINKEDIN = "LINKEDIN", "LinkedIn Message"

    contact = models.ForeignKey(
        Contact,
        on_delete=models.CASCADE,
        related_name="interactions"
    )

    interaction_type = models.CharField(
        max_length=20,
        choices=InteractionType.choices
    )

    notes = models.TextField()

    interaction_date = models.DateTimeField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.contact.name} - {self.interaction_type}"