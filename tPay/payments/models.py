from django.db import models


class Image(models.Model):
    student_number = models.CharField(max_length=30)
    image = models.ImageField(upload_to='images')


class PaymentRecord(models.Model):
    student_number = models.CharField(max_length=30)
    item = models.CharField(max_length=256)
    price_in_cents_cad = models.IntegerField(max_length=256)

    # human readable names
    class Meta:
        verbose_name = "Payment Record"
        verbose_name_plural = "Payment Records"


class Item(models.Model):
    item = models.CharField(max_length=256)
    price_in_cents_cad = models.IntegerField(max_length=256)

    # human readable names
    class Meta:
        verbose_name = "Item"
        verbose_name_plural = "Items"