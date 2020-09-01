from django.contrib.auth.models import User
from django.db import models

class Chart(models.Model):
    title = models.CharField(max_length=30)


class Point(models.Model):
    name = models.CharField(max_length=30)
    xaxis = models.DateField()
    yaxis = models.DecimalField(decimal_places=2, max_digits=9)
    chart = models.ForeignKey(Chart, on_delete=models.CASCADE)
