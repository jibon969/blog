import csv
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from .models import Blog, BlogSubCategory, Comment
from .forms import BlogForm, CommentForm, BlogCategory, SubCategoryCreateForm, CategoryCreateForm


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


def blog_category(request, slug):
    """
    This function based view work for show all category related post
    :param request:
    :param slug:
    :return:
    """
    obj = get_object_or_404(BlogCategory, slug=slug)
    queryset = Blog.objects.filter(category__slug=obj)
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
        'queryset_list': queryset,
        'search': search,
    }
    return render(request, "home/home.html", context)


def blog_sub_category(request, cat_slug, sub_cat_slug):
    """
    This function based view work for category & sub category related post
    :param request:
    :param cat_slug:
    :param sub_cat_slug:
    :return:
    """
    category_id = get_object_or_404(BlogCategory, slug__icontains=cat_slug)
    sub_category_id = get_object_or_404(BlogSubCategory, slug__icontains=sub_cat_slug)
    queryset = Blog.objects.filter(category=category_id, sub_category=sub_category_id)
    # Shorting Product
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
        'queryset_list': queryset,
        'search': search,
    }
    return render(request, "home/home.html", context)


def blog_detail(request, slug):
    """
    This function based view work for details page
    :param request:
    :param slug:
    :return:
    """
    post = get_object_or_404(Blog, slug=slug)
    recent_post = Blog.objects.all().order_by('-timestamp')[:6]
    """
    # Comment Queryset
    https://djangocentral.com/creating-comments-system-with-django/
    """
    comments = post.comments.filter(approve=True)
    new_comment = None
    # Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            messages.add_message(request, messages.SUCCESS, "Comment successfully sent, Thanks")
            new_comment.save()
    else:
        comment_form = CommentForm()
    context = {
        'object': post,
        'recent_post': recent_post,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form
    }
    return render(request, "home/details.html", context)


"""=============================
        Blog Crud
=============================="""


def blog_list(request):
    """
    This function based view work for show all blog post
    :param request:
    :return:
    """
    queryset = Blog.objects.all()
    search = request.GET.get('q')
    if search:
        queryset = Blog.objects.filter(
            Q(title__icontains=search) |
            Q(description=search) |
            Q(title__startswith=search) |
            Q(title__endswith=search)
        ).distinct()
    # print(search)
    # Pagination
    paginator = Paginator(queryset, 12)
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
    }
    return render(request, "home/crud/blog/blog_list.html", context)


def add_blog(request):
    """
    This function based view work for added new post
    :param request:
    :return:
    """
    form = BlogForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.add_message(request, messages.SUCCESS, "Blog added successfully uploaded !")
        return redirect('blog-list')
    else:
        form = BlogForm()
    context = {
        'form': form,
    }
    return render(request, "home/crud/blog/blog_form.html", context)


def update_blog(request, id):
    """
    This function based view work for update blog post
    :param request:
    :param id:
    :return:
    """
    obj = get_object_or_404(Blog, pk=id)
    form = BlogForm(request.POST or None, request.FILES or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.add_message(request, messages.SUCCESS, 'Blog successfully Updated')
        return redirect('blog-list')
    return render(request, "home/crud/blog/blog_form.html", {'form': form})


def delete_blog(request, id):
    """
    This function based view work for delete single item
    :param request:
    :param id:
    :return:
    """
    obj = get_object_or_404(Blog, pk=id)
    context = {
        'obj': obj
    }
    if request.method == "POST":
        obj.delete()
        messages.add_message(request, messages.WARNING, "Successfully Delete Blog !")
        return redirect('blog-list')
    return render(request, "home/crud/blog/delete_blog.html", context)


"""====================================================
            Blog Category CRUD Operations
====================================================="""


def blog_category_list(request):
    """
    This function based view work for showing all category list
    :param request: category_list
    :return: sub_category_list.html
    """
    category_queryset = BlogCategory.objects.all()
    query = request.GET.get('q')
    if query:
        category_queryset = BlogCategory.objects.filter(
            Q(title__icontains=query)
        )
    page = request.GET.get('page', 1)
    paginator = Paginator(category_queryset, 10)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(page)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        'object_list': posts,
        'page': page,
    }
    return render(request, "home/crud/category/category_list.html", context)


def blog_category_form(request):
    if request.method == "POST":
        form = CategoryCreateForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "Category Successfully Update ")
            return redirect('blog-category-list')
    else:
        form = CategoryCreateForm()
    context = {
        'form': form,
    }
    return render(request, "home/crud/category/category_form.html", context)


def blog_update_category(request, id):
    """
    This function based view works for update single item
    :param request: category_update
    :param id:
    :return: sub_category_form.html
    """
    page = request.GET.get("page")
    obj = get_object_or_404(BlogCategory, pk=id)
    form = CategoryCreateForm(request.POST or None, request.FILES or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.add_message(request, messages.SUCCESS, 'Category successfully Updated')
        url = reverse_lazy("blog-category-list") + "?page=" + page
        return redirect(url)
    context = {
        'form': form
    }
    return render(request, "home/crud/category/category_form.html", context)


def blog_delete_category(request, id):
    """
    This function based view work for delete single item in category table
    :param request:
    :param id:
    :return: delete_brand.html
    """
    obj = get_object_or_404(BlogCategory, pk=id)
    context = {
        'obj': obj
    }
    if request.method == "POST":
        obj.delete()
        messages.add_message(request, messages.SUCCESS, "Successfully Delete Category ! ")
        return redirect('blog-category-list')
    return render(request, "home/crud/category/delete_category.html", context)


def blog_download_category_csv(request):
    queryset = BlogCategory.objects.all()
    response = HttpResponse(content_type="text/csv")
    writer = csv.writer(response)
    writer.writerow([
        "ID", "Title"
    ])
    for category in queryset:
        row = []
        row.extend([
            category.id, category.title
        ])
        writer.writerow(row[:])
    response['Content-Disposition'] = 'attachment; filename="blog_category.csv"'
    return response


"""====================================================
            Blog SubCategory CRUD Operations
====================================================="""


def blog_sub_category_list(request):
    """
    This function based view work for showing all category list
    :param request: category_list
    :return: sub_category_list.html
    """
    category_queryset = BlogSubCategory.objects.all()
    query = request.GET.get('q')
    if query:
        category_queryset = BlogSubCategory.objects.filter(
            Q(title__icontains=query)
        )
    page = request.GET.get('page', 1)
    paginator = Paginator(category_queryset, 10)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(page)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        'object_list': posts,
        'page': page,
    }
    return render(request, "home/crud/sub_category/sub_category_list.html", context)


def blog_sub_category_form(request):
    if request.method == "POST":
        form = SubCategoryCreateForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "Category Successfully Update ")
            return redirect('blog-category-list')
    else:
        form = SubCategoryCreateForm()
    context = {
        'form': form,
    }
    return render(request, "home/crud/sub_category/sub_category_form.html", context)


def blog_sub_update_category(request, id):
    """
    This function based view works for update single item
    :param request: category_update
    :param id:
    :return: sub_category_form.html
    """
    page = request.GET.get("page")
    obj = get_object_or_404(BlogSubCategory, pk=id)
    form = CategoryCreateForm(request.POST or None, request.FILES or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.add_message(request, messages.SUCCESS, 'Category successfully Updated')
        url = reverse_lazy("blog-category-list") + "?page=" + page
        return redirect(url)
    context = {
        'form': form
    }
    return render(request, "home/crud/sub_category/sub_category_form.html", context)


def blog_sub_delete_category(request, id):
    """
    This function based view work for delete single item in category table
    :param request:
    :param id:
    :return: delete_brand.html
    """
    obj = get_object_or_404(BlogSubCategory, pk=id)
    context = {
        'obj': obj
    }
    if request.method == "POST":
        obj.delete()
        messages.add_message(request, messages.SUCCESS, "Successfully Delete Category ! ")
        return redirect('blog-category-list')
    return render(request, "home/crud/sub_category/delete_sub_category.html", context)


def blog_sub_download_category_csv(request):
    queryset = BlogSubCategory.objects.all()
    response = HttpResponse(content_type="text/csv")
    writer = csv.writer(response)
    writer.writerow([
        "ID", "Title"
    ])
    for category in queryset:
        row = []
        row.extend([
            category.id, category.title
        ])
        writer.writerow(row[:])
    response['Content-Disposition'] = 'attachment; filename="blog_sub_category.csv"'
    return response


"""=================================
        Comment Crud
================================="""


def blog_comment(request):
    queryset = Comment.objects.all()
    search = request.GET.get('q')
    if search:
        queryset = Comment.objects.filter(
            Q(name__icontains=search) |
            Q(name__contains=search) |
            Q(body__icontains=search) |
            Q(body__contains=search) |
            Q(email__icontains=search) |
            Q(email__contains=search)
        ).distinct()
    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 10)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(page)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        'object_list': posts,
        'page': page,
    }
    return render(request, "home/crud/comment/comment.html", context)


def update_comment(request, id):
    obj = get_object_or_404(Comment, pk=id)
    form = CommentForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.add_message(request, messages.SUCCESS, 'Comment successfully approve ')
        return redirect('blog-comment')
    return render(request, "home/crud/comment/comment_form.html", {'form': form})


def delete_comment(request, id):
    """
    This function based view work for delete single item
    :param request:
    :param id:
    :return:
    """
    obj = get_object_or_404(Comment, id=id)
    context = {
        'obj': obj
    }
    if request.method == "POST":
        obj.delete()
        messages.add_message(request, messages.WARNING, "Successfully Delete Comment !")
        return redirect('blog-comment')
    return render(request, "home/crud/comment/comment_delete.html", context)


def dashboard(request):
    return render(request, "home/dashboard.html")



