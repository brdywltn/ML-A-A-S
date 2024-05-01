# decorators.py
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.shortcuts import redirect

def user_type_required(user_type):
    def decorator(view_func):
        def wrap(request, *args, **kwargs):
            if request.user.is_superuser or request.user.profile.user_type == user_type:
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, 'You do not have permission to access this page.')
                return redirect('index') 
        return wrap
    return decorator

admin_required = user_type_required(1)
ml_engineer_required = user_type_required(2)
accountant_required = user_type_required(3)


def login_required(view_func):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, 'You must be logged in to access this page.')
            return redirect('login') 
    return wrap

def admin_accountant_required(view_func):
    def wrap(request, *args, **kwargs):
        if request.user.is_superuser or request.user.profile.user_type in [1, 3]:
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, 'You do not have permission to access this page.')
            return redirect('index') 
    return wrap

def admin_ml_engineer_required(view_func):
    def wrap(request, *args, **kwargs):
        if request.user.is_superuser or request.user.profile.user_type in [1, 2]:
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, 'You do not have permission to access this page.')
            return redirect('index') 
    return wrap