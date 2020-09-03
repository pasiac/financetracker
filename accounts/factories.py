from factory.django import DjangoModelFactory
import factory
from factory.fuzzy import FuzzyText
from django.contrib.auth.models import User

class UserFactory(DjangoModelFactory):
    username = factory.Sequence('testuser{}'.format)
    email = factory.Sequence('testuser{}@company.com'.format)
    

    class Meta:
        model = User