from django.shortcuts import render, redirect
from django.template import RequestContext

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.models import User
from django.contrib import messages

from .forms import CustomRegistrationForm, LoginForm


def index(request):
    return render(request, 'index.html')

def users(request):
    return render(request, 'user_page.html')

def handler404(request, *args, **kwargs):
    response = render(request, '404.html', {})
    response.status_code = 404
    return response

def handler500(request, *args, **kwargs):
    response = render(request, '500.html', {})
    response.status_code = 500
    return response

def maintenance(request):
    return render(request, 'maintenance.html')

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)  # Passing request along with username and password

            if user:
                login(request, user=user)  # Passing request along with user
                return redirect('users')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            pass

    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_login')
    else:
        form = CustomRegistrationForm()

    return render(request, 'register.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('user_login')
