from django.conf import settings
from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter
from rest_framework_simplejwt import views as jwt_views

from theinkspot.users.api.views import CategoryFollow, RegisterUsers, VerifyEmail

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("category", CategoryFollow, basename="categryFollow")

app_name = "api-users"

urlpatterns = [
    path("register/", RegisterUsers.as_view(), name="register"),
    path("token/", jwt_views.TokenObtainPairView.as_view(), name="access token"),
    path("refresh/token/", jwt_views.TokenRefreshView.as_view(), name="refresh token"),
    path("verify-email/", VerifyEmail.as_view(), name="verify-email"),
]

urlpatterns += router.urls
