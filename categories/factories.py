import factory
from factory.django import DjangoModelFactory

from accounts.factories import UserFactory
from categories.models import Category


class CategoryFactory(DjangoModelFactory):
    title = factory.Sequence(lambda n: "title_%d" % n)
    created_by = factory.SubFactory(UserFactory)

    class Meta:
        model = Category
