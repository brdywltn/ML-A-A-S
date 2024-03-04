# from django.db import models

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
    

