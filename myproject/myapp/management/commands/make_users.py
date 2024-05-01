# app/management/commands/create_users.py
from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from myapp.models import Profile

class Command(BaseCommand):
    def handle(self, *args, **options):
        User = get_user_model()
        
        if not User.objects.filter(username="superuser").exists():
            superuser = User.objects.create_superuser("superuser", password="placeholder")
            Profile.objects.filter(user=superuser).update(user_type=1)  
        
        if not User.objects.filter(username="admin").exists():
            admin = User.objects.create_user("admin", password="placeholder")
            Profile.objects.filter(user=admin).update(user_type=1)  
        
        if not User.objects.filter(username="base_user").exists():
            base_user = User.objects.create_user("base_user", password="placeholder")
            # No need to update user type for base_user as it defaults to Basic User (0)
        
        if not User.objects.filter(username="ml_engineer").exists():
            ml_engineer = User.objects.create_user("ml_engineer", password="placeholder")
            Profile.objects.filter(user=ml_engineer).update(user_type=2)  
        
        if not User.objects.filter(username="accountant").exists():
            accountant = User.objects.create_user("accountant", password="placeholder")
            Profile.objects.filter(user=accountant).update(user_type=3)  