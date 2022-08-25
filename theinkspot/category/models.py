from django.db import models
from django.utils.translation import gettext_lazy as _
from django_extensions.db.models import TimeStampedModel


class Category(TimeStampedModel):
    CATEGORIES = [
        ("sports", "Sports"),
        ("computer science", "Computer Science"),
        ("Physics", "Physics"),
        ("space", "Space"),
        ("cinema", "Cinema"),
        ("music", "Music"),
        ("economy", "Economy"),
    ]

    name = models.CharField(
        _("Category Name"), max_length=50, choices=CATEGORIES, unique=True
    )

    def __str__(self):
        return f"{self.name}"
