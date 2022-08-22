from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

# LOCAL IMPORTS GOES HERE!
from .utils import get_header_pic_url, get_profile_pic_url, resize


class Profile(models.Model):
    # https://www.merixstudio.com/blog/django-models-declaring-list-available-choices-right-way/
    class Colors(models.TextChoices):
        BLACK = "#000000", _("Black")
        WHITE = "#FFFFFF", _("White")

    class Meta:
        verbose_name = _("Profile")
        ordering = ["-created_at"]

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    about_text = models.TextField()
    profile_pic = models.ImageField(
        upload_to=get_profile_pic_url, blank=True, null=True
    )
    header_pic = models.ImageField(upload_to=get_header_pic_url, blank=True, null=True)
    short_bio = models.CharField(max_length=255, default="no bio")
    profile_views = models.IntegerField(default=0)
    accent_color = models.CharField(
        max_length=7, choices=Colors.choices, default=Colors.WHITE
    )
    background_color = models.CharField(
        max_length=7, choices=Colors.choices, default=Colors.WHITE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user}'s profile"

    def save(self, *args, **kwargs):
        resize(self.profile_pic, (200, 200))
        resize(self.header_pic, (200, 200))
        super().save(*args, **kwargs)
