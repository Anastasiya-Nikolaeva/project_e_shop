from django.urls import path

from .views import (
    CustomLoginView,
    CustomLogoutView,
    DeleteUserView,
    LogoutConfirmView,
    RegisterView,
    edit_profile,
)

app_name = "users"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("logout/confirm/", LogoutConfirmView.as_view(), name="logout_confirm"),
    path("delete/", DeleteUserView.as_view(), name="delete_user"),
    path("profile/edit/", edit_profile, name="edit_profile"),
]
