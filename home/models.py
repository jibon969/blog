from ckeditor.fields import RichTextField
from django.db import models
from django.db.models.signals import pre_save
from .utils import blog_unique_slug_generator


class BlogBanner(models.Model):
    title = models.CharField(max_length=120, blank=True, null=True, help_text='Banner title')
    largeDevices = models.ImageField(upload_to='blog/', null=True, blank=True, help_text="1400x400")
    mediumDevices = models.ImageField(upload_to='blog/', null=True, blank=True, help_text="800X400")
    smallDevices = models.ImageField(upload_to='blog/', null=True, blank=True, help_text="600x400")
    url_field = models.URLField(max_length=120, null=True, blank=True)
    value = models.IntegerField(null=True, blank=True, verbose_name="Position")
    timestamp = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
