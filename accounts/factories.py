import factory
from django.contrib.auth.models import User
from factory.django import DjangoModelFactory


class UserFactory(DjangoModelFactory):
    username = factory.Sequence("testuser{}".format)
    email = factory.Sequence("testuser{}@company.com".format)

    class Meta:
        model = User
