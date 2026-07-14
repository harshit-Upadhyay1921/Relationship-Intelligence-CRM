from django.conf import settings
from django.db import transaction
from django.utils import timezone

from apps.contacts.models import Contact

from .prompts import interaction_summary_prompt, follow_up_suggestion_prompt
from .providers import GeminiProvider


def trigger_summary_generation(contact):
    """
    Atomically transition STALE/NOT_GENERATED -> GENERATING and queue Celery task.
    Skips if generation is already in progress or the summary is ready.
    """
    from .tasks import generate_interaction_summary

    with transaction.atomic():
        locked_contact = Contact.objects.select_for_update().get(pk=contact.pk)

        if locked_contact.summary_status not in (
            Contact.SummaryStatus.STALE,
            Contact.SummaryStatus.NOT_GENERATED,
        ):
            return locked_contact

        locked_contact.summary_status = Contact.SummaryStatus.GENERATING
        locked_contact.save(update_fields=["summary_status"])

        contact_id = locked_contact.id
        transaction.on_commit(
            lambda: generate_interaction_summary.delay(contact_id)
        )

    return locked_contact


class AIInteractionSummaryService:

    @staticmethod
    def generate_summary(contact):

        interactions = contact.interactions.order_by("interaction_date")

        interaction_text = "\n".join(
            [
                f"{interaction.interaction_date} - "
                f"{interaction.interaction_type}: "
                f"{interaction.notes}"
                for interaction in interactions
            ]
        )

        prompt = interaction_summary_prompt(interaction_text)

        provider = GeminiProvider(settings.GEMINI_API_KEY)

        summary = provider.generate(prompt)

        updated = Contact.objects.filter(
            pk=contact.pk,
            summary_status=Contact.SummaryStatus.GENERATING,
        ).update(
            ai_summary=summary,
            summary_generated_at=timezone.now(),
            summary_status=Contact.SummaryStatus.READY,
        )

        if updated:
            return summary

        return None

class AIFollowUpSuggestionService:

    @staticmethod
    def generate_suggestion(contact):

        latest_interaction = (
            contact.interactions.order_by("-interaction_date")
            .first()
        )

        latest_interaction_text = ""

        if latest_interaction:
            latest_interaction_text = (
                f"{latest_interaction.interaction_date} - "
                f"{latest_interaction.interaction_type}: "
                f"{latest_interaction.notes}"
            )

        prompt = follow_up_suggestion_prompt(
            contact.ai_summary,
            latest_interaction_text,
        )

        provider = GeminiProvider(settings.GEMINI_API_KEY)

        return provider.generate(prompt)