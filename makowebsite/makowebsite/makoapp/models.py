# models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class Role(models.Model):
    role_name = models.CharField(max_length=255)
    role_description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.role_name

class User(AbstractUser):
    user_name = models.CharField(max_length=255)
    user_contact = models.CharField(max_length=20)
    user_email = models.EmailField(unique=True)
    user_address = models.CharField(max_length=255)
    user_image = models.ImageField(upload_to='user_images/', null=True, blank=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user_name



class Property(models.Model):
    property_name = models.CharField(max_length=255)
    property_description = models.CharField(max_length=255)
    property_price = models.DecimalField(max_digits=10, decimal_places=2)
    property_image = models.ImageField(upload_to='property_images/', null=True, blank=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='properties')
    is_sold = models.BooleanField(default=False) 

    def __str__(self):
        return self.property_name


class Document(models.Model):
    documentation_type = models.CharField(max_length=255)
    documentation_image = models.ImageField(upload_to='document_images/', null=True, blank=True) 
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
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