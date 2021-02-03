from django.contrib import admin
from import_export import resources
from .models import BlogBanner, BlogCategory, BlogSubCategory, Blog, Comment
from import_export.admin import ImportExportModelAdmin


class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'timestamp']
    search_fields = ['title']
    list_per_page = 10

    class Meta:
        model = BlogCategory


admin.site.register(BlogCategory, BlogCategoryAdmin)


class BlogSubCategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'timestamp']
    search_fields = ['title']
    list_per_page = 10

    class Meta:
        model = BlogSubCategory


admin.site.register(BlogSubCategory, BlogSubCategoryAdmin)


class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'timestamp']
    search_fields = ['title']
    list_per_page = 10

    class Meta:
        model = Blog


admin.site.register(Blog, BlogAdmin)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'post', 'created_on', 'approve')
    list_filter = ('approve', 'created_on')
    search_fields = ('name', 'email', 'body')
    list_editable = ['approve']
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(approve=True)


class BlogBannerResource(resources.ModelResource):
    class Meta:
        model = BlogBanner
        fields = ('id', 'largeDevices', 'mediumDevices', 'smallDevices', 'value', 'url_field')


class BlogBannerResourceAdmin(ImportExportModelAdmin):
    resource_class = BlogBannerResource
    list_display = ['title', 'url_field', 'value', 'timestamp']
    list_editable = ['value']


admin.site.register(BlogBanner, BlogBannerResourceAdmin)