from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
	path('', views.home_view, name='home'),
	path("login/", views.user_login, name="login"),
	path("logout/", views.logout_view, name="logout"),
	path("signup/", views.signup, name="signup"),
	path("profile/", views.profile, name="profile"),
	path('profile/delete/', views.delete_account, name='delete_account'),
	path("history/", views.history_view, name="history"),
	path("notifications/", views.notifications_view, name="notifications"),
]
