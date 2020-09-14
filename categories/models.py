from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=30)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name
