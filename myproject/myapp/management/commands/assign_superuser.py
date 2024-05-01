from django.core.management.base import BaseCommand
from myapp.models import Profile

class Command(BaseCommand):
    help = 'Assigns superuser status to users with user type 1'

    def handle(self, *args, **options):
        profiles = Profile.objects.filter(user_type=1)
        for profile in profiles:
            user = profile.user
            user.is_superuser = True
            user.is_staff = True
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Assigned superuser status to {user.username}'))