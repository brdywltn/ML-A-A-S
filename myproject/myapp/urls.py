from django.urls import path

<<<<<<< HEAD
from .views import InstrumentDetectionView, index, users, maintenance, handler404, handler500, terms_conditions, privacy_policy, handling_music_file, pricing, generate_pdf, admin_table
=======
from .views import InstrumentDetectionView, index, users, maintenance, handler404, handler500, register, user_login, terms_conditions, privacy_policy, handling_music_file, pricing, generate_pdf, admin_table
from .payments import create_payment, execute_payment, payment_cancelled, payment_success
from django.contrib.auth import views as auth_views

# Authentication
from .views import RegisterView, CustomLoginView
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', index, name='index'),
    path('user/', users, name='users'),
    path('404/', handler404, name='handler404'),
    path('500/', handler500),
    path('maintenance/', maintenance),
    # path('register/', register, name='register'),
    # path('login/', user_login, name='user_login'),
    path('terms_conditions/', terms_conditions, name='terms_conditions'),
    path('pricay_policy/', privacy_policy, name='privacy_policy'),
    path('pricing/', pricing, name='pricing'),
    path('uploading_file/', handling_music_file, name='uploading_file'),
    path('generate_pdf/', generate_pdf, name='generate_pdf'),
    path('pricing/', pricing, name='pricing'),
    path('generate_pdf/', generate_pdf, name='generate_pdf'),
    path('admin_table/', admin_table, name='admin_table'),
    path('instrument_detection/', InstrumentDetectionView.as_view(), name='instrument_detection'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='password_change_form.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'), name='password_change_done'),
    # path('user_logout/', auth_views.LogoutView.as_view(next_page='index'), name='user_logout'),
    path('payment/create/', create_payment, name='create_payment'),
    path('payment/execute/', execute_payment, name='execute_payment'),
    path('payment/cancel/', payment_cancelled, name='payment_cancelled'),
    path('payment_success/', payment_success, name='success')

    # Authentication
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('user_logout/', auth_views.LogoutView.as_view(next_page='index'), name='user_logout'),
    path('payment/create/', create_payment, name='create_payment'),
    path('payment/execute/', execute_payment, name='execute_payment'),
    path('payment/cancel/', payment_cancelled, name='payment_cancelled'),
    path('payment_success/', payment_success, name='success')
]
