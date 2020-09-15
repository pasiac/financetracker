import factory
from django.contrib.auth.models import User
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyText


class UserFactory(DjangoModelFactory):
    username = FuzzyText(length=5)
    email = factory.Faker("ascii_company_email", locale="pl_PL")

    class Meta:
        model = User
