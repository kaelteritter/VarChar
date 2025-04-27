from django.contrib import auth
from django.shortcuts import redirect, render


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