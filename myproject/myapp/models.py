from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from enum import Enum

class Action(Enum):
    UPLOAD_FILE = 'upload_file'
    LOGIN = 'login'
    REGISTER = 'register'
    PAYMENT = 'payment'
    GENERATE_FINANCIAL_STATEMENT = 'generate_financial_statement'
    CHANGE_MLA = 'change_MLA'
    RUN_ALGORITHM = 'run_algorithm'
    INVALID_FILE = 'invalid_file'
    INVALID_PASSWORD = 'invalid_password'
    USER_DOES_NOT_EXIST = 'user_does_not_exist'
    DOWNLOAD_BREAKDOWN = 'download_breakdown'
    UNKNOWN = 'unknown'
# #   Usertypes
# #   ---------
# #   0 - Basic User
# #   1 - Admin
# #   2 - ML Engineer
# #   3 - Accountant

# # Create your models here.
# class User(models.Model):
#     """
#     *   User model
#     """
#     username = models.CharField(max_length=150)
#     password = models.CharField(max_length=16)
#     email = models.EmailField(max_length=200)
#     usertype = models.ForeignKey("UserType", on_delete=models.DO_NOTHING)

# class UserType(models.Model):
#     """
#     *   Usertype model
#     """
#     usertype = models.CharField(max_length=15)


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
