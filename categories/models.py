from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=30)
    created_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    def get_related_expenses_value_list(self):
        return self.expense_set.values_list("value", flat=True)

    def __str__(self):
        return self.title
