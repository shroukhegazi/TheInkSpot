from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CategoryConfig(AppConfig):
    name = "theinkspot.category"
    verbose_name = _("Category")

    def ready(self):
        try:
            import theinkspot.users.signals  # noqa F401
        except ImportError:
            pass
