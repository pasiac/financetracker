from decimal import Decimal

from django.test import TestCase

from accounts.factories import UserFactory
from expense.factories import ExpenseFactory
from expense.models import Expense
from utils.tests.mixins import TestUtilityMixin


class TestEdit(TestCase, TestUtilityMixin):
    def setUp(self):
        self.user = UserFactory.create()
        self.expense = ExpenseFactory.create(created_by=self.user)
        self.url = f"/wydatki/edytuj/{self.expense.id}/"

    def test_user_cant_enter_edit_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertNotEqual(response.status_code, self.STATUS_OK)

    def test_user_can_see_edit_form_after_log_in(self):
        self.__given_user_logged_in()
        response = self.client.get(self.url)
        self.assertContains(response, "Edycja wydatku")

    def test_user_redirected_after_success_edit(self):
        self.__given_user_logged_in()
        response = self.client.post(
            self.url, {"title": "new title", "value": Decimal("99.21")}
        )
        self.__then_expense_title_and_value_changed()
        self.__then_redirected_to_expense_list(response)

    def test_user_get_404_when_edit_non_existing_expense(self):
        self.__given_user_logged_in()
        non_existing_expense_id = self.expense.id + 1
        url = f"wydatki/edytuj/{non_existing_expense_id}"
        response = self.client.post(
            url, {"title": "new title", "value": Decimal("99.21")}
        )
        self.assertEqual(response.status_code, self.STATUS_NOT_FOUND)

    def __given_user_logged_in(self):
        self.client.force_login(self.user, backend=None)

    def __then_expense_title_and_value_changed(self):
        expense = Expense.objects.get(pk=self.expense.id)
        self.assertEqual(expense.title, "new title")
        self.assertEqual(expense.value, Decimal("99.21"))

    def __then_redirected_to_expense_list(self, response):
        self.was_redirected_to("/wydatki/", response)
