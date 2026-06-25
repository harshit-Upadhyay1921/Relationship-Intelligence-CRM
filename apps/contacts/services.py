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

    @staticmethod
    def needs_follow_up(contact):
        last_interaction_date = RelationshipScoringService.get_last_interaction(contact)
        
        if not last_interaction_date:
            return True

        days_since_last_interaction = ((timezone.now() - last_interaction_date).days)

        return days_since_last_interaction > 30
