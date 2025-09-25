from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/core/", include("core.urls")),  # 👈 add this
    path("api/dashboard/", include("dashboard.urls")),  # keep your dashboard
]
