from django.test import TestCase

from accounts.factories import UserFactory
from expense.factories import ExpenseFactory
from utils.tests.mixins import TestUtilityMixin


class TestEdit(TestCase, TestUtilityMixin):
    def setUp(self):
        self.user = UserFactory.create()
        self.expense = ExpenseFactory.create(created_by=self.user)
        self.url = f"/wydatki/{self.expense.id}/"

    def test_access_forbiden_if_user_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, self.STATUS_FORBIDDEN)

    def test_view_with_chart(self):
        self.__given_user_logged_in()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, self.STATUS_OK)
        self.assertContains(response, "pie-chart")
        self.assertContains(response, self.expense.title)

    def __given_user_logged_in(self):
        self.client.force_login(self.user, backend=None)
