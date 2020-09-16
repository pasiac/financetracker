from django.test import TestCase

from accounts.factories import UserFactory
from categories.factories import CategoryFactory
from utils.tests.mixins import TestUtilityMixin
from expense.factories import ExpenseFactory


class TestEdit(TestCase, TestUtilityMixin):
    def setUp(self):
        self.user = UserFactory.create()
        self.category = CategoryFactory.create(created_by=self.user)
        self.url = f"/kategorie/{self.category.id}/"

    def test_access_forbiden_if_user_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, self.STATUS_FORBIDDEN)

    def test_view_without_chart_if_category_isnt_related_to_any_expense(self):
        self.__given_user_logged_in()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, self.STATUS_OK)
        self.assertNotContains(response, "pie-chart")

    def test_view_with_chart(self):
        self.__given_user_logged_in()
        ExpenseFactory.create(category=self.category)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, self.STATUS_OK)
        self.assertContains(response, "pie-chart")
        self.assertContains(response, self.category.title)

    def __given_user_logged_in(self):
        self.client.force_login(self.user, backend=None)
