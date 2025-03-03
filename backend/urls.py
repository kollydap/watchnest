from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("core.urls")),
    path(
        "api/v1/auth/", include("dj_rest_auth.urls")
    ),  # Login, logout, password reset, etc.
    path("api/v1/auth/signup/", include("dj_rest_auth.registration.urls")),  # Signup
]
