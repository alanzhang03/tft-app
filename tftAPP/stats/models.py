from django.db import models

# Create your models here.

class Augment(models.Model):
    name = models.CharField(max_length=30)

    games_total = models.IntegerField()
    games_two_one = models.IntegerField()
    games_three_two = models.IntegerField()
    games_four_two = models.IntegerField()

    avg_total = models.DecimalField(max_digits=3, decimal_places=2)
    avg_two_one = models.DecimalField(max_digits=3, decimal_places=2)
    avg_three_two = models.DecimalField(max_digits=3, decimal_places=2)
    avg_four_two = models.DecimalField(max_digits=3, decimal_places=2)



