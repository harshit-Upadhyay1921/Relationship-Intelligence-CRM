from django.contrib import admin

from .models import Company

class CompanyAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "website",
        "industry",
    )

    list_filter = (
        "name",
        "industry",
    )

    search_fields = (
        "name",
        "website",
    )
admin.site.register(Company, CompanyAdmin)
