from django.db import models
from django.utils.translation import gettext_lazy as _

"""
Defines a User model with unique usernames and automatic timestamp fields for creation and update.

Fields:
- username: Unique identifier for the user, required.
- created_at: Automatically set to the time when the user instance is created.
- updated_at: Automatically updated every time the user instance is saved.
"""

class User(models.Model):
    username = models.CharField(_("username"), max_length=25, unique=True, blank=False, null=False)

    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)
