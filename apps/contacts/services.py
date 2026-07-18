from django.utils import timezone

class RelationshipScoringService:
    @staticmethod
    def calculate_relationship_score(last_interaction_date):
        if not last_interaction_date:
            return 0
        
        days_since_last_interaction = (timezone.now() - last_interaction_date).days
        
        if days_since_last_interaction < 7:
            return 100
        elif days_since_last_interaction < 30:
            return 75
        elif days_since_last_interaction < 60:
            return 50
        elif days_since_last_interaction < 180:
            return 25
        else:
            return 0

    @staticmethod
    def get_last_interaction(contact):
        last_interaction = contact.interactions.order_by("-interaction_date").first()
        return last_interaction.interaction_date if last_interaction else None


# Note:
# `needs_follow_up()` is intentionally not kept in this service.
# Relationship score calculation is non-trivial business logic, so it belongs here.
# However, `needs_follow_up` is now just a simple derived property:
#
#     relationship_score < 50
#
# It is defined directly on the Contact model as a @property to avoid
# duplicating trivial logic across the codebase.
#
# This is actually a cleaner architecture than what the course suggests.
# It follows the principle of keeping simple derived properties on the model
# while reserving the service layer for non-trivial business logic.


import csv

from django.http import HttpResponse


class CSVExportService:

    @staticmethod
    def export_contacts(queryset):

        response = HttpResponse(
            content_type="text/csv"
        )

        response["Content-Disposition"] = (
            'attachment; filename="contacts.csv"'
        )

        writer = csv.writer(response)

        writer.writerow(
            [
                "Name",
                "Email",
                "Phone",
                "Status",
                "Relationship Score",
            ]
        )

        for contact in queryset:
            writer.writerow(
                [
                    contact.name,
                    contact.email,
                    contact.phone,
                    contact.status,
                    contact.relationship_score,
                ]
            )

        return response