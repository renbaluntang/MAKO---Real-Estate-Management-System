from django.contrib import admin
from .models import Role, User, Property, Document, TransactionHistory

# Register your models here.
admin.site.register(Role)
admin.site.register(User)
admin.site.register(Property)
admin.site.register(Document)
admin.site.register(TransactionHistory)