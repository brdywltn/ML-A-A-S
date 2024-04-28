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
    INVALID_FILE = "{username} uploaded an invalid file that cannot be processed."
    INVALID_PASSWORD = "{username} has entered an invalid password."
    USER_DOES_NOT_EXIST = "The user {username} does not exist in the system."
    DOWNLOAD_BREAKDOWN = "{username} has downloaded a breakdown of their data."
    UNKNOWN = "An unknown error has occurred for user {username}."

# class Logs(models.Model):
#     """
#     *   Logs model
#     """
#     user_id = models.ForeignKey("User", on_delete=models.CASCADE)
#     error_id = models.IntegerField()
#     date = models.DateTimeField()

# class Feedback(models.Model):
#     """
#     *   Feedback Model
#     """
#     user_id = models.ForeignKey("User", on_delete=models.CASCADE)
#     content = models.CharField(max_length=2000)
#     date = models.DateTimeField()

# class Bills(models.Model):
#     """
#     *   Bill/receipts Model
#     """
#     user_id = models.ForeignKey("User", on_delete=models.CASCADE)
#     date = models.DateTimeField()
#     paid = models.BooleanField(default=False)


# class Files(models.Model):
#     """
#     *   Uploaded files
#     """
#     date = models.DateTimeField()
#     data = models.CharField(max_length=2000)
#     uploader = models.ForeignKey("User", on_delete=models.CASCADE)

class Audio(models.Model):
    file = models.FileField('audio', upload_to='audio')

class Log(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    log = models.JSONField()


# # LOGIN
# log_data = get_log_data(Action.LOGIN, 'success', user=request.user.username)
# create_log(log_data)
# # REGISTER
# log_data = get_log_data(Action.REGISTER, 'success', user=request.user.username)
# create_log(log_data)
# # INVALID_PASSWORD
# log_data = get_log_data(Action.INVALID_PASSWORD, 'error', user=request.user.username)
# create_log(log_data)
# # GENERATE_FINANCIAL_STATEMENT
# log_data = get_log_data(Action.GENERATE_FINANCIAL_STATEMENT, 'success', user=request.user.username)
# create_log(log_data)
