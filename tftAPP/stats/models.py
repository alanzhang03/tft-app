from django.db import models

# Create your models here.

class Augment(models.Model):
    name = models.CharField(max_length=30)

    games_total = models.IntegerField(default=0)
    games_two_one = models.IntegerField(default=0)
    games_three_two = models.IntegerField(default=0)
    games_four_two = models.IntegerField(default=0)

    avg_total = models.FloatField(default=None, null=True)
    avg_two_one = models.FloatField(default=None, null=True)
    avg_three_two = models.FloatField(default=None, null=True)
    avg_four_two = models.FloatField(default=None, null=True)
