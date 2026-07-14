from celery import shared_task

from apps.contacts.models import Contact
from .services import AIInteractionSummaryService


@shared_task(bind=True, max_retries=2, default_retry_delay=30)
def generate_interaction_summary(self, contact_id):
    try:
        contact = Contact.objects.get(id=contact_id)
    except Contact.DoesNotExist:
        return

    if contact.summary_status != Contact.SummaryStatus.GENERATING:
        return

    try:
        AIInteractionSummaryService.generate_summary(contact)
    except Exception as exc:
        Contact.objects.filter(
            id=contact_id,
            summary_status=Contact.SummaryStatus.GENERATING,
        ).update(summary_status=Contact.SummaryStatus.STALE)

        raise self.retry(exc=exc)
