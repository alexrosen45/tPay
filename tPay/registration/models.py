from django.db import models  

class Person(models.Model):
    first_name = models.CharField(max_length=50, default=None)
    last_name = models.CharField(max_length=50, default=None)
    student_number = models.CharField(max_length=50, default=None)
    image = models.ImageField(null=True, blank=True, upload_to="images/")

    # human readable names
    class Meta:
        verbose_name = "Person"
        verbose_name_plural = "People"