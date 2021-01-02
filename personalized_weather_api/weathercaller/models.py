from django.db import models

class Day(models.Model):
    token = models.CharField(max_length=10)
    date = models.DateField()
    data = models.CharField(max_length=100)
