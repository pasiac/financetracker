from factory.django import DjangoModelFactory
import factory
from factory.fuzzy import FuzzyText
from expense.models import Expense
import datetime


class ExpenseFactory(DjangoModelFactory):
    title = factory.Sequence(lambda n: "title_%d" % n)
    value = factory.fuzzy.FuzzyDecimal(low=1)
    date = datetime.datetime.now()

    class Meta:
        model = Expense
