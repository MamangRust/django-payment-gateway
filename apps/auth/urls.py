from django.urls import path
from .views import LoginView, RegisterView, profile
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path("profile/", profile, name="profile"),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
]
