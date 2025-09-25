from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path("auth/signup", views.signup, name="signup"),
    path("auth/login", views.login_user, name="login"),

    # User
    path("dashboard", views.get_dashboard, name="dashboard"),
    path("user/referral", views.get_referral, name="referral"),
    path("user/submit", views.submit_assignment, name="submit_assignment"),
    path("user/withdraw", views.withdraw, name="withdraw"),

    # Admin (JWT auth + is_staff)
    path("admin/users", views.admin_users, name="admin_users"),
    path("admin/verify-user", views.admin_verify_user, name="admin_verify_user"),
    path("admin/post", views.admin_post_assignment, name="admin_post_assignment"),
]
