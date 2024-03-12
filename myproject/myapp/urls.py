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
from .views import handling_music_file


from .views import pricing
from .views import generate_pdf
from .views import generate_pdf

urlpatterns = [
    # path('', index, name='index'), <- uncomment when index/main page will be ready
    path('', index),
    path('user/', users, name='users'),
    path('404/', handler404),
    path('500/', handler500),
    path('maintenance/', maintenance),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('terms_conditions/', terms_conditions, name='terms_conditions'),
    path('pricay_policy/', privacy_policy, name='privacy_policy'),
    path('pricing/', pricing, name='pricing'),
    path('uploading_file/', handling_music_file, name='uploading_file'),
,
    path('generate_pdf/', generate_pdf, name='generate_pdf')
]
