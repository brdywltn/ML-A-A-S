from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User, Group, Permission 
from django.contrib.contenttypes.models import ContentType

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

