from .models import AuditLog


class AuditService:

    @staticmethod
    def log_action(user, contact, action, description):
        AuditLog.objects.create(
            user=user,
            contact=contact,
            action=action,
            description=description,
        )