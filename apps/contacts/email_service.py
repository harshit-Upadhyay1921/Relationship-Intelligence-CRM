from django.core.mail import send_mail


class EmailService:

    @staticmethod
    def send_follow_up_email(contact):

        send_mail(
            subject=f"Follow up with {contact.name}",
            message=f"You should follow up with {contact.name}.",
            from_email=None,
            recipient_list=[contact.email],
        )