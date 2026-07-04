from google.auth.transport import requests
from google.oauth2 import id_token

from django.conf import settings

from apps.users.models import User

from google.auth.exceptions import GoogleAuthError

from apps.integrations.models import GoogleAccount

class GoogleAuthService:

    @staticmethod
    def authenticate_google_user(id_token_value, access_token):

        try:
            payload = id_token.verify_oauth2_token(
                        id_token_value,
                        requests.Request(),
                        settings.GOOGLE_CLIENT_ID,
            )
        except GoogleAuthError:
            return None

        email = payload["email"]

        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                "username": email,
                "first_name": payload.get("given_name", ""),
                "last_name": payload.get("family_name", ""),
            },
        )
        GoogleAccount.objects.update_or_create(
            user=user,
            defaults={
                "google_id": payload["sub"],
                "access_token": access_token,
            },
    )

        return user