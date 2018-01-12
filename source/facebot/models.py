from django.db import models
from django_extensions.db.models import TimeStampedModel
from django.contrib.postgres.fields import JSONField


class FacePage(TimeStampedModel):
    page_id = models.CharField(unique=True, max_length=128)
    url = models.URLField()
    page_name = models.CharField(max_length=512)
    profile_picture = models.ImageField(upload_to='pictures/profile', blank=True, null=True)
    cover_picture = models.ImageField(upload_to='pictures/profile', blank=True, null=True)
    phone_number = models.CharField(max_length=128, blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=256, blank=True, null=True)
    hours = JSONField(blank=True, null=True)


class PagePost(TimeStampedModel):
    page_post_id = models.CharField(max_length=32, unique=True)
    created_time = models.DateTimeField()
    message = models.TextField(blank=True, null=True)


class TimelineImage(TimeStampedModel):
    post = models.ForeignKey(PagePost, blank=True, null=True, on_delete=models.CASCADE)
    timeline_image_id = models.CharField(max_length=32, unique=True)
    created_time = models.DateTimeField()
    image = models.ImageField(upload_to='pictures/timeline', blank=True, null=True)
