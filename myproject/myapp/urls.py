from django.urls import path
from .views import index, users, maintenance, handler404, handler500, register, user_login



urlpatterns = [
    # path('', index, name='index'), <- uncomment when index/main page will be ready
    path('', index),
    path('user/',users, name='users'),
    path('404/', handler404),
    path('500/', handler500),
    path('maintenance/', maintenance),
    path('register/', register, name='register'),
    path('login/', user_login, name='user_login'),
]

