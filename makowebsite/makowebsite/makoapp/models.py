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
    
    def is_admin(self):
        return self.role and self.role.role_name == 'Admin' 
    
    def is_buyer(self):
        return self.role and self.role.role_name == 'Buyer' 
    
    def is_seller(self):
        return self.role and self.role.role_name == 'Seller' 
    pass



class Property(models.Model):
    property_name = models.CharField(max_length=255)
    property_description = models.CharField(max_length=255)
    property_price = models.DecimalField(max_digits=10, decimal_places=2)
    property_image = models.ImageField(upload_to='property_images/', null=True, blank=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='properties')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='properties_bought', null=True, blank=True)
    is_reserved = models.BooleanField(default=False) 


    def __str__(self):
        return self.property_name

    def sell_property(self, buyer):
        self.buyer = buyer
        self.is_reserved = True
        self.save()


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
    
class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='property_images/', null=True, blank=True)

    def __str__(self):
        return f"Image for {self.property.property_name}"