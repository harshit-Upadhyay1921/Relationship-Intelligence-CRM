from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter

from rest_framework.permissions import IsAuthenticated

from rest_framework import viewsets


from .models import Contact
from .serializers import ContactSerializer

from apps.audit.models import AuditLog
from apps.audit.services import AuditService

from django.utils import timezone

from rest_framework.decorators import action
from rest_framework.response import Response

class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]

    filterset_fields = ['status', 'category']
    ordering_fields = ["name","created_at",]
    search_fields = ["name","email","job_title",]

    def get_queryset(self):
        return Contact.objects.filter(
            owner=self.request.user,
            is_deleted=False,
        )
    def perform_create(self, serializer):
        contact = serializer.save(owner=self.request.user)

        AuditService.log_action(
            user=self.request.user,
            contact=contact,
            action=AuditLog.Action.CREATE,
            description=f"Contact '{contact.name}' created.",
        )
    def perform_update(self, serializer):
        contact = serializer.save()

        AuditService.log_action(
            user=self.request.user,
            contact=contact,
            action=AuditLog.Action.UPDATE,
            description=f"Updated contact '{contact.name}'",
        
        )
    def perform_destroy(self, instance):
        instance.is_deleted=True
        instance.deleted_at=timezone.now()
        instance.save()

    @action(detail=True, methods=["post"])
    def restore(self, request, pk=None):
        contact = Contact.objects.filter(
            owner=request.user,
            is_deleted=True,
            pk=pk,
        ).first()

        if not contact:
            return Response(
                {"detail": "Contact not found."},
                status=404,
            )

        contact.is_deleted = False
        contact.deleted_at = None
        contact.save()

        return Response({"message": "Contact restored successfully."})
