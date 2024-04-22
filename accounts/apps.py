from django.apps import AppConfig

"""
Configuration for the accounts application, using BigAutoField as the default field type for model IDs.
"""

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'
