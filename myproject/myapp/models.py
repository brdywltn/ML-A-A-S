from django.db import models
#from django.contrib.auth import get_user_model
from django.contrib.auth.models import User#, Group, Permission
#from django.contrib.contenttypes.models import ContentType
from enum import Enum
from django.dispatch import receiver
from django.db.models.signals import post_save

class Profile(models.Model):
    USER_TYPES = (
        (0, 'Basic User'),
        (1, 'Admin'),
        (2, 'ML Engineer'),
        (3, 'Accountant'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.IntegerField(choices=USER_TYPES, default=0)

    def __str__(self):
        return f'{self.user.username} Profile'

# Model to hold the user token count
class UserTokenCount(models.Model):
    # User
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Token count
    token_count = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user.username}\'s token count: {self.token_count}'
    
# Automatically create a UserTokenCount and a account type Profile table entry for each user on user creation
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserTokenCount.objects.get_or_create(user=instance)
        Profile.objects.get_or_create(user=instance)
    # instance.profile.save()

class Action(Enum):
    UPLOAD_FILE = "The user has successfully uploaded a file."
    LOGIN = "The user has logged in to their account."
    REGISTER = "The user has registered for a new account."
    PAYMENT_SUCCESSFUL = "The user has successfully made a payment."
    GENERATE_FINANCIAL_STATEMENT = "The user has generated a financial statement."
    CHANGE_MLA = "The user has changed their maximum loss amount (MLA)."
    RUN_ALGORITHM = "The user has run an algorithm."
    INVALID_FILE = "The uploaded file is invalid and cannot be processed."
    INVALID_PASSWORD = "The user has entered an invalid password."
    USER_DOES_NOT_EXIST = "The user does not exist in the system."
    DOWNLOAD_BREAKDOWN = "The user has downloaded a breakdown of their data."
    UNKNOWN = "An unknown error has occurred."

class Audio(models.Model):
    file = models.FileField('audio', upload_to='audio')

class Log(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    log = models.JSONField()
