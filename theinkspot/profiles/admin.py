from django.contrib import admin

# lOCAL IMPORTS GOES HERE!
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "created_at")
    list_filter = ("created_at", "user")
