from django.contrib import admin

from theinkspot.posts.models import Post, TaggedPost


# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["tags"]

    search_fields = ["tags"]


@admin.register(TaggedPost)
class PostTaggedAdmin(admin.ModelAdmin):
    list_display = ["content_object"]
