from django.db import models
from django.contrib.auth.models import AbstractUser

class Role(models.Model):
    role_name = models.CharField(max_length=255)
    role_description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.role_name

class Permissions(models.Model):
    permission_name = models.CharField(max_length=255)
    permission_perks = models.CharField(max_length=255)
    permission_role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='permissions')

    def __str__(self):
        return self.permission_name

class User(AbstractUser):
    user_name = models.CharField(max_length=255)
    user_contact = models.CharField(max_length=20)
    user_email = models.EmailField(unique=True)
    user_address = models.CharField(max_length=255)
    user_username = models.CharField(max_length=255, unique=True)
    user_password = models.CharField(max_length=255)
    user_image = models.ImageField(upload_to='user_images/', null=True, blank=True)
    role = models.OneToOneField(Role, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user_name

class Property(models.Model):
    property_name = models.CharField(max_length=255)
    property_description = models.CharField(max_length=255)
    property_price = models.DecimalField(max_digits=10, decimal_places=2)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='properties')

    def __str__(self):
        return self.property_name

class Document(models.Model):
    documentation_type = models.CharField(max_length=255)
    property = models.OneToOneField(Property, on_delete=models.CASCADE)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents_sold', null=True, blank=True)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents_bought', null=True, blank=True)

    def __str__(self):
        return self.documentation_type

class TransactionHistory(models.Model):
    transaction_date = models.DateField()
    transaction_desc = models.CharField(max_length=255)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions_sold')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions_bought')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='transactions')

    def __str__(self):
        return f"Transaction on {self.transaction_date}"