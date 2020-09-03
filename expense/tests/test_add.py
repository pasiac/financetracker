from decimal import Decimal

from django.test import TestCase

from accounts.factories import UserFactory
from expense.factories import ExpenseFactory
from expense.models import Expense
from utils.tests.mixins import TestUtilityMixin


class TestViewExpenseAdd(TestCase, TestUtilityMixin):
    url = "/wydatki/dodaj/"

    def setUp(self):
        self.user = UserFactory.create()
        self.existing_expense = ExpenseFactory.create(created_by=self.user)
        self.new_expense_data = {
            "title": "New test expense",
            "value": Decimal("111.11"),
        }

    def test_not_loged_in_user_cant_add(self):
        response = self.client.post(self.url, self.new_expense_data)
        self.assertNotEqual(response.status_code, self.STATUS_OK)

    def test_get_expense_form(self):
        self.client.force_login(self.user, backend=None)

        url = self.url.format(self.existing_expense.id)
        response = self.client_send_request_with_params(url, self.new_expense_data)
        self.assertEqual(response.status_code, self.STATUS_OK)

    def test_add_expense_when_missing_required_data_fails(self):
        self.client.force_login(self.user, backend=None)

        missing_expense_data = {
            "title": "Wont work no value",
        }

        response = self.client_send_post_request(self.url, missing_expense_data)
        self.assertFalse(response.context["form"].is_valid())

    def test_add_expense_ok(self):
        self.client.force_login(self.user, backend=None)

        response = self.client.post(self.url, self.new_expense_data)
        created_expense = Expense.objects.get(pk=self.existing_expense.pk + 1)
        expected_location = "/wydatki/"
        self.assertTrue(self.was_redirected_to(expected_location, response))
        self.assertEqual(created_expense.title, self.new_expense_data["title"])
        self.assertEqual(
            created_expense.value,
            self.new_expense_data["value"],
        )
