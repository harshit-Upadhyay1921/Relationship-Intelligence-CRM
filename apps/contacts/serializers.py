from rest_framework import serializers

from .models import Contact
from .models import Company
from apps.companies.serializers import CompanySerializer


class ContactSerializer(serializers.ModelSerializer):
    company = serializers.PrimaryKeyRelatedField(
        queryset=Company.objects.all(),
        required=False,
        allow_null=True,
    )

    relationship_score = serializers.ReadOnlyField()
    needs_follow_up = serializers.ReadOnlyField()
    last_interaction_date = serializers.ReadOnlyField()

    class Meta:
        model = Contact
        fields = "__all__"
        read_only_fields = ["owner"]