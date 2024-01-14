from django.db import models

# Create your models here.

class Augment(models.Model):
    name = models.CharField(max_length=30)
    two_one = models.DecimalField(max_digits=3, decimal_places=2)
    three_two = models.DecimalField(max_digits=3, decimal_places=2)
    four_two = models.DecimalField(max_digits=3, decimal_places=2)
