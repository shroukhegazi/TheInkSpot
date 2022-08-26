from django.conf import settings
from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter
from rest_framework_simplejwt import views as jwt_views

from theinkspot.users.api.views import (
    CategoryFollow,
    RegisterUsers,
    UserViewSet,
    VerifyEmail,
)

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet, "user")
router.register("users/category", CategoryFollow, basename="categryFollow")


app_name = "api-users"
urlpatterns = router.urls

urlpatterns += [
    path("users/register/", RegisterUsers.as_view(), name="register"),
    path("users/token/", jwt_views.TokenObtainPairView.as_view(), name="access token"),
    path(
        "users/refresh/token/",
        jwt_views.TokenRefreshView.as_view(),
        name="refresh token",
    ),
    path("users/verify-email/", VerifyEmail.as_view(), name="verify-email"),
]
