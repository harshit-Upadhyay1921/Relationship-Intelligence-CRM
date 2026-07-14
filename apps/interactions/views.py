from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .models import Interaction
from .serializers import InteractionSerializer

from apps.contacts.models import Contact
from apps.audit.services import AuditService
from apps.audit.models import AuditLog

permission_classes = [AllowAny]

class InteractionViewSet(viewsets.ModelViewSet):
    queryset = Interaction.objects.all()
    serializer_class = InteractionSerializer

    def perform_create(self, serializer):
        interaction = serializer.save()

        contact = interaction.contact

        contact.status = Contact.Status.ACTIVE
        contact.relationship_score = 100
        contact.summary_status = Contact.SummaryStatus.STALE
        contact.save(
            update_fields=[
                "status",
                "relationship_score",
                "summary_status",
            ]
        )

        AuditService.log_action(
            user=self.request.user,
            contact=contact,
            action=AuditLog.Action.UPDATE,
            description=f"Reactivated contact '{contact.name}' after new interaction.",
        )




# perform_create() in InteractionViewSet

# Creating a new interaction means the relationship becomes active again.
# Immediately reactivate the contact and reset its relationship score to 100
# instead of waiting for the nightly Celery recalculation.


# serializer.save() vs model.save()

# serializer.save()
# -----------------
# Creates/updates the model handled by the serializer using validated request data.
#
# model.save()
# ------------
# Persists any manual changes made after serializer.save(), such as updating
# related models (e.g. Contact status or relationship score).