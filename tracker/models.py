from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=30)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class IncomeOutcome(models.Model):
    title = models.CharField(max_length=30)
    value = models.DecimalField(decimal_places=2, max_digits=8)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, null=True, on_delete=models.CASCADE)

    def get_dict(self):
        return {
            "title": self.title,
            "value": self.value,
            "date": self.date,
            "category": self.category,
        }


class Chart(models.Model):
    title = models.CharField(max_length=30)


class Point(models.Model):
    name = models.CharField(max_length=30)
    xaxis = models.DateField()
    yaxis = models.DecimalField(decimal_places=2, max_digits=9)
    chart = models.ForeignKey(Chart, on_delete=models.CASCADE)
