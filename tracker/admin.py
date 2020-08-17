from django.contrib import admin

from tracker.models import Category, IncomeOutcome

# Register your models here.
admin.site.register(IncomeOutcome)
admin.site.register(Category)
