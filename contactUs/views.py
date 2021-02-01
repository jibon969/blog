from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import messages
from .forms import ContactForm
from .forms import ReplayForm
from .models import Contact
from django.conf import settings
from django.db.models import Q
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def contact(request):
    form = ContactForm(request.POST or None)
    errors = None
    if form.is_valid():
        form.save()
        messages.add_message(request, messages.SUCCESS, "Success! Thank you for your message.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    if form.errors:
        errors = form.errors
    context = {
        'form': form,
        'errors': errors
    }
    return render(request, 'contacts/contacts.html', context)


def contact_list(request):
    posts_list = Contact.objects.all()
    query = request.GET.get('q')
    page = request.GET.get('page')
    if query:
        posts_list = Contact.objects.filter(
            Q(subject__icontains=query) |
            Q(name__contains=query) |
            Q(email__icontains=query) |
            Q(phone__icontains=query)
        ).distinct()
    paginator = Paginator(posts_list, 10)  # 10 posts per page
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    context = {
        'posts': posts,
        'page': page
    }
    return render(request, 'contacts/contact_list.html', context)


def update_contact(request, id):
    obj = get_object_or_404(Contact, pk=id)
    form = ContactForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.add_message(request, messages.SUCCESS, 'Successfully updated Contact info.')
        return redirect('contact-list')
    return render(request, 'contacts/contact_update.html', {'form': form})


def delete_contact(request, id):
    if request.user.is_superuser:
        obj = get_object_or_404(Contact, pk=id)
        context = {
            'obj': obj
        }
        if request.method == "POST":
            obj.delete()
            messages.add_message(request, messages.WARNING, 'Successfully Delete this contact')
            return redirect("contact-list")
        return render(request, "contacts/delete_contact.html", context)
    else:
        messages.add_message(request, messages.WARNING, 'Only superuser and access this .')
        return redirect('home')


def replay_customer(request):
    if request.method == "POST":
        form = ReplayForm(request.POST or None)
        if form.is_valid():
            email = form.cleaned_data['send_to']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            send_mail(subject, message, settings.EMAIL_HOST_USER, [email])
            form.save()
            messages.success(request, 'your message has been sent')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        form = ReplayForm()
    return render(request, 'contacts/replay_email.html', {'form': form})







