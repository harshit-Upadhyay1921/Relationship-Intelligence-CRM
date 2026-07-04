"""
CUSTOM USER MODEL

Why are we doing this?

By default Django uses its own built-in User model.

However, in a real CRM we may later need fields such as:
- google_id
- phone_number
- profile_picture
- department
- role

Changing from Django's default User model to a custom User model
AFTER the project has grown is painful because:
- migrations already exist
- foreign keys already reference auth.User
- database tables already contain data

Therefore, we create a custom User model at the beginning of the project.

This model currently behaves exactly like Django's default User because
it inherits from AbstractUser and does not add any new fields yet.

AUTH_USER_MODEL = "users.User"

Format:
    app_label.ModelName

where:
    users -> Django app label
    User  -> model class name

Project structure:
    apps/
        users/
            models.py

Even though the folder path is apps/users,
Django identifies the app by its label:

    users

Therefore:

    AUTH_USER_MODEL = "users.User"

means:

    "Use the User model from the users app."

NOT:

    AUTH_USER_MODEL = "apps.users.User"

because Django uses the app label, not the folder path.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass