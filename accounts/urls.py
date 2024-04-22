from django.urls import path

from . import views
"""
URL configurations for the accounts app.
"""

app_name = "accounts"
urlpatterns = [
    path("pick_username/", views.pick_username, name="pick-username"),
]
