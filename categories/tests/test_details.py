from django.test import TestCase

from accounts.factories import UserFactory
from categories.factories import CategoryFactory
from categories.models import Category
from utils.tests.mixins import TestUtilityMixin


class TestEdit(TestCase, TestUtilityMixin):
    def setUp(self):
        self.user = UserFactory.create()
        self.category = CategoryFactory.create(created_by=self.user)
        self.url = f"/kategorie/{self.category.id}/"
