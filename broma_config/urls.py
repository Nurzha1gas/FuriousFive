from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("conversations.urls")),
    path("", include("accounts.urls")),
    path("", include("core.urls")),
]
"""
Defines URL patterns for the project, routing to admin, conversations, accounts, and core apps.
"""
