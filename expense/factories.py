import datetime

import factory
from factory.django import DjangoModelFactory

from accounts.factories import UserFactory
from expense.models import Expense


class ExpenseFactory(DjangoModelFactory):
    title = factory.Sequence(lambda n: "title_%d" % n)
    value = factory.fuzzy.FuzzyDecimal(low=1)
    date = datetime.datetime.now()
    created_by = factory.SubFactory(UserFactory)

    class Meta:
        model = Expense
