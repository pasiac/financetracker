from decimal import Decimal

from django.test import TestCase

from accounts.factories import UserFactory
from expense.factories import ExpenseFactory
from expense.models import Expense
from utils.tests.mixins import TestUtilityMixin


class TestDelete(TestCase, TestUtilityMixin):
    def setUp(self):
        self.user = UserFactory.create()
        self.expense = ExpenseFactory.create(created_by=self.user)
        self.url = f"/wydatki/usun/{self.expense.id}/"

    def test_user_cant_delete_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertNotEqual(response.status_code, self.STATUS_OK)

    def test_user_can_delete_after_log_in(self):
        self.__given_user_logged_in()
        before = Expense.objects.count()
        response = self.client.post(self.url)
        after = Expense.objects.count()
        self.assertEqual(before, after + 1)
        self.__then_redirected_to_expense_list(response)

    def test_user_get_404_when_delete_non_existing_expense(self):
        self.__given_user_logged_in()
        non_existing_expense_id = self.expense.id + 1
        url = f"wydatki/usun/{non_existing_expense_id}"
        response = self.client.post(url)
        self.assertEqual(response.status_code, self.STATUS_NOT_FOUND)

    def __given_user_logged_in(self):
        self.client.force_login(self.user, backend=None)

    def __then_redirected_to_expense_list(self, response):
        self.was_redirected_to("/wydatki/", response)
