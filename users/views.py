from django.contrib import auth
from django.shortcuts import redirect, render

from .forms import SignUpForm


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(request, username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            return render(request, 'users/login.html', {'error': 'Неверный логин или пароль!'})

    return render(request, 'users/login.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(**request.POST)
        if form.is_valid():
            form.save()
        return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'users/signup.html', {'form': form})