from django.conf import settings
from django.db import models


class GoogleAccount(models.Model):
    class Meta:
        verbose_name = "Google Account"
        verbose_name_plural = "Google Accounts"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="google_account",
    )

    google_id = models.CharField(
        max_length=255,
        unique=True,
    )

    access_token = models.TextField()

    refresh_token = models.TextField(
        blank=True,
        null=True,
    )

    token_expiry = models.DateTimeField(
        blank=True,
        null=True,
    )

    last_synced_at = models.DateTimeField(
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return self.user.email