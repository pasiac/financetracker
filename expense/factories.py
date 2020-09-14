import datetime

import factory
import factory.fuzzy
from factory.django import DjangoModelFactory

from accounts.factories import UserFactory
from expense.models import Expense


class ExpenseFactory(DjangoModelFactory):
    title = factory.Sequence(lambda n: "title_%d" % n)
    # AttributeError: module 'factory' has no attribute 'FuzzyDecimal'
    value = 10.20
    date = datetime.datetime.now()
    created_by = factory.SubFactory(UserFactory)

    class Meta:
        model = Expense
