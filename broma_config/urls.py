from django.contrib import admin
from django.urls import include, path
from django.contrib.auth.views import LoginView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("conversations.urls")),
    path("", include("accounts.urls")),
    path("", include("core.urls")),
]
