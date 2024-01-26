from django.contrib import auth
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import authenticate

from .forms import UserLoginForm


def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return redirect(to='product:index')
        else:
            print(form.errors)
    else:

        form = UserLoginForm()

    return render(request, 'users/login.html', {'form': form})


def logout(request):
    auth.logout(request)
    return redirect(to='product:index')
