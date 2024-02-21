from django.urls import path
from .views import index
from .views import users

urlpatterns = [
    path('', index, name='index'),
    path('user/',users)
]
