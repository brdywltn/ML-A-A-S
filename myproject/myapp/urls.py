from django.urls import path
from .views import index
from .views import users
from .views import maintenance
from .views import handler404
from .views import handler500
from .views import register
from .views import login
from .views import terms_conditions
from .views import privacy_policy




urlpatterns = [
    # path('', index, name='index'), <- uncomment when index/main page will be ready
    path('', index),
    path('user/',users, name='user'),
    path('404/', handler404),
    path('500/', handler500),
    path('maintenance/', maintenance),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('terms_conditions/', terms_conditions, name='terms_conditions'),
    path('pricay_policy/', privacy_policy, name='privacy_policy'),
    
]

