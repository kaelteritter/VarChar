from django.contrib import auth
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import LoginForm, SignUpForm


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data.get('user')
            auth.login(request, user)
            return redirect('/')
        else:
            return render(request, 'users/login.html', {'form': form})
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            return render(request, 'users/signup.html', {'form': form})
    else:
        form = SignUpForm()
    return render(request, 'users/signup.html', {'form': form})


def logout(request):
    auth.logout(request)
    return render(request, 'index.html')