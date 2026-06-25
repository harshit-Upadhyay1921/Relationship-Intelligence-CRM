from django.contrib import admin

from .models import Interaction

class InteractionAdmin(admin.ModelAdmin):
    list_display = (
        "contact",
        "interaction_type",
        "interaction_date",
    )

    list_filter = (
        "interaction_type",
        "interaction_date",
    )

    search_fields = (
        "contact__name",
        "contact__company__name",
    )
admin.site.register(Interaction, InteractionAdmin)
