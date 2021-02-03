from .models import Comment, Blog, BlogBanner, BlogCategory, BlogSubCategory
from django import forms


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = [
            'title',
            'image',
            'category',
            'description'
        ]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body', 'approve']


class BlogBannerForm(forms.ModelForm):
    class Meta:
        model = BlogBanner
        fields = [
            'title',
            'largeDevices',
            'mediumDevices',
            'smallDevices',
            'url_field',
            'value'
        ]


class CategoryCreateForm(forms.ModelForm):
    class Meta:
        model = BlogCategory
        fields = [
            'title',
        ]


class SubCategoryCreateForm(forms.ModelForm):
    class Meta:
        model = BlogSubCategory
        fields = [
            'title',
        ]

