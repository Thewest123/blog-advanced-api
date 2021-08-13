from django.urls import path
from .views import ChangePasswordView, UserLoginView, UserLogoutView


app_name = "core"

urlpatterns = [
    path("login/", UserLoginView.as_view()),
    path("logout/", UserLogoutView.as_view()),
    path("change-password/", ChangePasswordView.as_view()),
]
