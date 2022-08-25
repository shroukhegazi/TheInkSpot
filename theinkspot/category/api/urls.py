from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from theinkspot.category.api.views import CategoryViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("", CategoryViewSet, basename="category")


app_name = "api-category"
urlpatterns = router.urls
