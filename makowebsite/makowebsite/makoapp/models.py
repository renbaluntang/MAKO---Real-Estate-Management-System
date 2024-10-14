from django.db import models
from django.contrib.auth.models import AbstractUser

class Role(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class User(AbstractUser):
    user_name = models.CharField(max_length=100)
    user_contact = models.CharField(max_length=11)
    user_email = models.EmailField(unique=True)
    user_address = models.TextField()
    user_username = models.CharField(max_length=50, unique=True)
    user_password = models.CharField(max_length=50)
    user_image = models.ImageField(upload_to='user_images/', null=True, blank=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user_name