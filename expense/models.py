from django.contrib.auth.models import User
from django.db import models

from categories.models import Category


class Expense(models.Model):
    title = models.CharField(max_length=30)
    value = models.DecimalField(decimal_places=2, max_digits=8)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(
        Category, null=True, blank=True, on_delete=models.SET_NULL
    )
    recipe = models.ImageField(upload_to="img", null=True, blank=True)

    def __str__(self):
        return "{} with value {} added {} to {}.".format(
            self.title, self.value, self.date, self.category
        )
