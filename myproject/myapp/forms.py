from django import forms
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.models import User

class CustomRegistrationForm(UserCreationForm):
    #UserCreationForm comes with username, password1, password2 by default
    #only email needs to be added for our custom users
    email = forms.EmailField()

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["username", "email", "password1", "password2"]

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)