from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from enum import Enum

# class UserTypes(User):
#     USER_TYPE_CHOICES = (
#         0, 'Basic User',
#         1, 'Admin',
#         2, 'ML Engineer',
#         3, 'Accountant'
#     )

#     usertype = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES) # should we declare default=0 here?

# group_names = ['Basic User', 'Admin', 'ML Engineer', 'Accountant']
# for group_name in group_names:
#     Group.objects.get_or_create(name=group_name)

# assign group permissions
# content_type = ContentType.objects.get_for_model(UserTypes)
# permission = Permission.objects.create(codename='can_view_user',
#                                        name='Can View User',
#                                        content_type=content_type)
# group = Group.objects.get(name='Admin')
# group.permissions.add(permission)


# User = get_user_model()

# user = User.objects.create_user('username', 'email', 'password')
#names are not necessary - reduces gdpr concerns aswell


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
