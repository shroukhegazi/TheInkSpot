from django.urls import path
from rest_framework import routers

from .views import ChangePasswordView, ProfileModelViewSet

urlpatterns = [
    path(
        "change-password/<int:pk>/",
        ChangePasswordView.as_view(),
        name="ChangePasswordView",
    ),
]


router = routers.SimpleRouter()
router.register(r"user-profile", ProfileModelViewSet, basename="profiles")


urlpatterns += router.urls
