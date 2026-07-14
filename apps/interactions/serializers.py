from rest_framework import serializers
from .models import Interaction
from apps.contacts.models import Contact


class ContactSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = [
            "id",
            "name",
            "category",
            "status",
        ]


class InteractionSerializer(serializers.ModelSerializer):
    contact = ContactSummarySerializer(read_only=True)

    contact_id = serializers.PrimaryKeyRelatedField(
        source="contact",
        queryset=Contact.objects.all(),
        write_only=True,
    )

    class Meta:
        model = Interaction
        fields = "__all__"