from django.contrib import admin

from .models import Contact

class ContactAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "email",
        "company",
        "status",
        "category",
        "relationship_score",
        "last_interaction_date",
        "needs_follow_up",
    )

    list_filter = (
        "status",
        "category",
    )

    search_fields = (
        "name",
        "email",
    )

admin.site.register(Contact, ContactAdmin)


# from django.contrib import admin

# from .models import Contact


# @admin.register(Contact)
# class ContactAdmin(admin.ModelAdmin):
#     list_display = (
#         "name",
#         "email",
#         "company",
#         "category",
#         "status",
#     )

#     list_filter = (
#         "status",
#         "category",
#     )

#     search_fields = (
#         "name",
#         "email",
#     )


# NOTE: READ OUT FOR BETTER UNDERSTANDING OF THE @admin.register DECORATOR
# @admin.register(Contact) is a decorator that automatically registers
# the Contact model with this ContactAdmin class.
#
# Equivalent to:
#
# class ContactAdmin(admin.ModelAdmin):
#     ...
#
# admin.site.register(Contact, ContactAdmin)
#
# Note:
# admin.site.register(Contact) alone only registers the model and uses
# Django's default admin page. It will NOT apply list_display,
# list_filter, search_fields, or any other custom admin settings.