from django.shortcuts import render
from .models import BlogBanner
# Create your views here.


def home(request):
    queryset = BlogBanner.objects.all().order_by('-timestamp')
    context = {
        'object_list': queryset,
    }
    return render(request, "home/home.html", context)