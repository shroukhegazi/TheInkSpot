from django.contrib import admin

from theinkspot.category.models import Category


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "created", "modified"]


admin.site.register(Category, CategoryAdmin)
