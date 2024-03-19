from django.urls import path
from .views import index, users, maintenance, handler404, handler500, register, user_login, terms_conditions, privacy_policy, handling_music_file, pricing, generate_pdf, admin_table
from django.contrib.auth import views as auth_views

urlpatterns = [
    # path('', index, name='index'), <- uncomment when index/main page will be ready
    path('', index),
    path('user/', users, name='users'),
    path('404/', handler404),
    path('500/', handler500),
    path('maintenance/', maintenance),
    path('register/', register, name='register'),
    path('login/', user_login, name='user_login'),
    path('terms_conditions/', terms_conditions, name='terms_conditions'),
    path('pricay_policy/', privacy_policy, name='privacy_policy'),
    path('pricing/', pricing, name='pricing'),
    path('uploading_file/', handling_music_file, name='uploading_file'),
    path('generate_pdf/', generate_pdf, name='generate_pdf'),
    path('pricing/', pricing, name='pricing'),
    path('generate_pdf/', generate_pdf, name='generate_pdf'),
    path('admin_table/', admin_table, name='admin_table'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='password_change_form.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'), name='password_change_done'),
]
