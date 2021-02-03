from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from . forms import RegisterUserForm


def get_register(request):
    form = RegisterUserForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, 'Registration successfully completed')
        return redirect('login')
    return render(request, 'accounts/register.html', {"form": form})


def get_login(request):
    if request.method == "POST":
        user = request.POST.get('user')
        password = request.POST.get('pass')
        auth = authenticate(request, username=user, password=password)
        if auth is not None:
            login(request, auth)
            messages.add_message(request, messages.SUCCESS, 'You have successfully logged in ')
            return redirect("home")
        else:
            messages.add_message(request, messages.ERROR, "Please enter the username and register correctly")
    return render(request, 'accounts/login.html')


def logout_view(request):
    messages.add_message(request, messages.WARNING, "You have successfully logged out!")
    logout(request)
    return redirect('home')