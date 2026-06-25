from rest_framework import serializers

from .models import Contact
from apps.companies.serializers import CompanySerializer


class ContactSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    relationship_score = serializers.ReadOnlyField()
    needs_follow_up = serializers.ReadOnlyField()
    last_interaction_date = serializers.ReadOnlyField()
    class Meta:
        model = Contact
        fields = "__all__"