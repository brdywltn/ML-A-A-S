# models.py
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
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


class Action(Enum):
    UPLOAD_FILE = "{username} has successfully uploaded a file."
    LOGIN = "{username} has logged in to their account."
    REGISTER = "{username} has registered for a new account."
    PAYMENT_SUCCESSFUL = "{username} has successfully made a payment."
    GENERATE_FINANCIAL_STATEMENT = "{username} has generated a financial statement."
    CHANGE_MLA = "{username} has changed their maximum loss amount (MLA)."
    RUN_ALGORITHM = "{username} has run an algorithm."
    FEEDBACK_SUBMITTED = "{username} has submitted feedback."
    INVALID_FILE = "{username} uploaded an invalid file that cannot be processed."
    INVALID_PASSWORD = "{username} has entered an invalid password."
    USER_DOES_NOT_EXIST = "The user {username} does not exist in the system."
    DOWNLOAD_BREAKDOWN = "{username} has downloaded a breakdown of their data."
    UNKNOWN = "An unknown error has occurred for user {username}."

class Audio(models.Model):
    file = models.FileField('audio', upload_to='audio')

class Log(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    log = models.JSONField()
    feedback = models.BooleanField(null=True)

class ModelConfig(models.Model):
    selected_model_version = models.CharField(max_length=255, default='2')

    def save(self, *args, **kwargs):
        # Ensure there's only one instance of ModelConfig
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

class ModelPerformanceMetrics(models.Model):
    request_count = models.IntegerField(default=0)
    request_latency_sum = models.FloatField(default=0)
    request_latency_count = models.IntegerField(default=0)
    runtime_latency_sum = models.FloatField(default=0)
    runtime_latency_count = models.IntegerField(default=0)
    model_load_latency = models.FloatField(default=0)

    def reset_metrics(self):
        self.request_count = 0
        self.request_latency_sum = 0
        self.request_latency_count = 0
        self.runtime_latency_sum = 0
        self.runtime_latency_count = 0
        self.model_load_latency = 0
        self.save(force_update=True)

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_id = models.CharField(max_length=255)
    payer_id = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Payment by {self.user.username} - Amount: {self.amount}'

