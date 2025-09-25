from django.urls import path
from . import views

urlpatterns = [
    path("auth/signup", views.signup, name="signup"),
    path("auth/login", views.login_user, name="login"),
    path("dashboard", views.dashboard, name="dashboard"),
]
