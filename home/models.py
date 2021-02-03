from ckeditor.fields import RichTextField
from django.db import models
from django.db.models.signals import pre_save
from .utils import blog_unique_slug_generator
from PIL import Image


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

    class Meta:
        ordering = ['-timestamp']


class BlogCategory(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(null=True, blank=True, max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-timestamp']


def blog_category_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = blog_unique_slug_generator(instance)


pre_save.connect(blog_category_pre_save_receiver, sender=BlogCategory)


class BlogSubCategory(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(null=True, blank=True, max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-timestamp']


def blog_sub_category_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = blog_unique_slug_generator(instance)


pre_save.connect(blog_sub_category_pre_save_receiver, sender=BlogSubCategory)


class Blog(models.Model):
    title = models.CharField(max_length=120, blank=True, null=True)
    image = models.ImageField(upload_to="blog/", blank=True, null=True)
    category = models.ForeignKey(BlogCategory, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(BlogSubCategory, on_delete=models.CASCADE, blank=True, null=True)
    description = RichTextField(blank=True, null=True)
    slug = models.SlugField(null=True, blank=True, max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-timestamp']

    # def save(self, *arg, **kwargs):
    #     super().save(*arg, **kwargs)
    #     img = Image.open(self.image.path)
    #     if img.height > 350 or img.weight > 350:
    #         output_size = (350, 350)
    #         img.thumbnail(output_size)
    #         img.save(self.image.path)

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     img = Image.open(self.image.path)
    #     height = 200
    #     weight = 400
    #     output_size = (height, weight)
    #     img.thumbnail(output_size)
    #     img.save(self.image.path)


def blog_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = blog_unique_slug_generator(instance)


pre_save.connect(blog_pre_save_receiver, sender=Blog)


class Comment(models.Model):
    post = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField(blank=True, null=True)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    approve = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)


