from rest_framework import serializers

from .models import Contact
from .models import Company
# from apps.companies.serializers import CompanySerializer
from apps.audit.serializers import AuditLogSerializer

class ContactSerializer(serializers.ModelSerializer):
    
    company = serializers.PrimaryKeyRelatedField(
        queryset=Company.objects.all(),
        required=False,
        allow_null=True,
    )
    audit_logs = AuditLogSerializer(
        many=True,
        read_only=True,
    )
    # This was correct when relationship_score was a @property. Now you've changed it to a database field-> relationship_score = models.PositiveIntegerField(default=0). So you don't need to declare it manually anymore.
    # relationship_score = serializers.ReadOnlyField() 
    needs_follow_up = serializers.ReadOnlyField()
    last_interaction_date = serializers.ReadOnlyField()

    follow_up_suggestion = serializers.SerializerMethodField()

    def get_follow_up_suggestion(self, obj):

        request = self.context.get("request")

        if not request:
            return None

        if not self.context.get("include_follow_up_suggestion"):
            return None

        if obj.summary_status != Contact.SummaryStatus.READY:
            return None

        if not obj.ai_summary:
            return None

        from apps.ai.services import AIFollowUpSuggestionService

        return AIFollowUpSuggestionService.generate_suggestion(obj)
    class Meta:
        model = Contact
        fields = "__all__"
        read_only_fields = ["owner"]