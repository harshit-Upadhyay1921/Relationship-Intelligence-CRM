from celery import shared_task

from .models import Contact

from .email_service import EmailService

from .services import RelationshipScoringService
from apps.contacts.models import Contact
from apps.ai.services import AIInteractionSummaryService

@shared_task
def check_follow_ups():
    contacts = Contact.objects.filter(
        is_deleted=False,
    )

    follow_up_contacts = []

    for contact in contacts:
        if contact.needs_follow_up:
            follow_up_contacts.append(contact.name)
            EmailService.send_follow_up_email(contact)

    print(f"Needs Follow Up: {follow_up_contacts}")


@shared_task
def recalculate_relationship_scores():
    contacts = Contact.objects.filter(is_deleted=False)

    for contact in contacts:
        contact.relationship_score = RelationshipScoringService.calculate_relationship_score(
            contact.last_interaction_date
        )
        contact.save(update_fields=["relationship_score"])
        print(contact.name, contact.relationship_score)


@shared_task
def mark_dormant_contacts():
    contacts = Contact.objects.filter(
        is_deleted=False,
    )

    for contact in contacts:
        if contact.relationship_score <= 25:
            contact.status = Contact.Status.DORMANT
            contact.save(update_fields=["status"])

    