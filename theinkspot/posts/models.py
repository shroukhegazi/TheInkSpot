from django.db import models
from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase


class TaggedPost(TaggedItemBase):
    content_object = models.ForeignKey("Post", on_delete=models.CASCADE)


class Post(models.Model):
    tags = TaggableManager()
