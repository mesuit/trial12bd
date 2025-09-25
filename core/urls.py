from django.urls import path
from . import views

urlpatterns = [
    path("auth/signup/", views.signup),
    path("auth/login/", views.login),
    path("dashboard/", views.dashboard),
    path("assignments/submit/", views.submit_assignment),
]
