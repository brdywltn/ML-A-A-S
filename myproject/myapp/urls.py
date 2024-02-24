from django.urls import path
from .views import index
from .views import users
from .views import maintenance
from .views import handler404
from .views import handler500

urlpatterns = [
    path('', index, name='index'),
    path('user/',users),
    path('404/', handler404),
    path('500/', handler500),
    path('maintenance/', maintenance)
]

