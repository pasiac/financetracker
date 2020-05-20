import factory
import factory.fuzzy
from django.contrib.auth.models import User
from factory.django import DjangoModelFactory

from .models import Category, IncomeOutcome


class UserFactory(DjangoModelFactory):

    username = factory.Sequence("testuser{}".format)
    email = factory.Sequence("testuser{}@company.com".format)

    class Meta:
        model = User


class CategoryFactory(DjangoModelFactory):
    name = factory.Sequence("category{}".format)
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = Category


class IncomeOutcomeFactory(DjangoModelFactory):
    title = factory.Sequence("item{}".format)
    value = factory.fuzzy.FuzzyDecimal(low=1)
    user = factory.SubFactory(UserFactory)
    category = factory.SubFactory(CategoryFactory)

    class Meta:
        model = IncomeOutcome
