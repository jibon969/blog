from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from .models import BlogBanner, Blog, BlogCategory, BlogSubCategory
from random import randint


def home(request):
    queryset = Blog.objects.all()
    queryset_list = Blog.objects.all().order_by('timestamp')[:2]
    search = request.GET.get('q')
    if search:
        queryset = Blog.objects.filter(
            Q(title__icontains=search) |
            Q(description=search) |
            Q(title__startswith=search) |
            Q(title__endswith=search)
        ).distinct()
    # Pagination
    paginator = Paginator(queryset, 6)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    context = {
        'object_list': posts,
        'page': page,
        'queryset_list': queryset_list,
        'search': search,
    }
    return render(request, "home/home.html", context)