from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import BlogBanner


class BlogBannerResource(resources.ModelResource):
    class Meta:
        model = BlogBanner
        fields = ('id', 'largeDevices', 'mediumDevices', 'smallDevices', 'value', 'url_field')


class BlogBannerResourceAdmin(ImportExportModelAdmin):
    resource_class = BlogBannerResource
    list_display = ['title', 'url_field', 'value', 'timestamp']
    list_editable = ['value']


admin.site.register(BlogBanner, BlogBannerResourceAdmin)
