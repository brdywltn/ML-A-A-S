from django.db import models

#   Usertypes
#   ---------
#   0 - Basic User
#   1 - Admin
#   2 - ML Engineer
#   3 - Accountant

# Create your models here.
# class User(models.Model):
#     """
#     *   User model
#     """
#     username = models.CharField(max_length=150)
#     password = models.CharField(max_length=16)
#     email = models.EmailField(max_length=200)
#     #usertype = models.ForeignKey("UserType")

# class UserType(models.Model):
#     """
#     *   Usertype model
#     """
#     usertype = models.CharField(max_length=15)

# class Logs(models.Model):
#     """
#     *   Logs model
#     """
#     content = models.CharField(max_length=2000)
#     #user_id = models.ForeignKey("User")
#     date = models.DateTimeField()

# class Feedback(models.Model):
#     """
#     *   Feedback Model
#     """
#     #user_id = models.ForeignKey("User")
#     content = models.CharField(max_length=2000)
#     date = models.DateTimeField()

# class Bills(models.Model):
#     """
#     *   Bill/receipts Model
#     """
#     #user_id = models.ForeignKey("User")
#     date = models.DateTimeField()
#     paid = models.BooleanField(default=False)

