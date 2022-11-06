from django.contrib import admin
from .models import PaymentRecord, Item

admin.site.register(PaymentRecord)
admin.site.register(Item)