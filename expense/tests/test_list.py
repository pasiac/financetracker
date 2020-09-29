from django.test import TestCase

from accounts.factories import UserFactory
from expense.factories import ExpenseFactory
from utils.tests.mixins import TestUtilityMixin


class TestList(TestCase, TestUtilityMixin):
    url = "/wydatki/"

    def setUp(self):
        self.user = UserFactory.create()
        self.expense_per_page = 10
        self.paging_element = "paging_grip"

    def test_user_cant_see_expense_list_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertNotEqual(response.status_code, self.STATUS_OK)

    def test_user_can_see_his_expenses_after_log_in(self):
        self.__given_user_logged_in()
        self.__given_expenses_created(title="test expense")
        response = self.client.get(self.url)
        self.__then_logged_in_user_expenses_shown(response)

    def test_returns_ok_when_there_are_multiple_page_of_expenses(
        self,
    ):
        self.__given_user_logged_in()
        ExpenseFactory.create_batch(
            size=self.expense_per_page + 1, created_by=self.user
        )

        response = self.client.get(self.url)
        self.assertEqual(self.STATUS_OK, response.status_code)
        self.assertContains(response, "&laquo;")

    def test_returns_matched_item(self):
        self.__given_user_logged_in()
        self.__given_expenses_created(title="item")
        url = f"{self.url}?title__icontains=item"
        response = self.client.get(url)
        self.assertEqual(self.STATUS_OK, response.status_code)
        self.assertContains(response, "item")

    def test_returns_no_items_if_no_one_match(self):
        self.__given_user_logged_in()
        self.__given_expenses_created(title="test")
        url = f"{self.url}?title__icontains=noexisting"
        response = self.client.get(url)
        self.assertEqual(self.STATUS_OK, response.status_code)
        self.assertNotContains(response, "test")

    def __given_user_logged_in(self):
        self.client.force_login(self.user, backend=None)

    def __given_expenses_created(self, **kwargs):
        ExpenseFactory.create(**kwargs, created_by=self.user)
        ExpenseFactory.create(title="other user expense")

    def __then_logged_in_user_expenses_shown(self, response):
        self.assertEqual(response.status_code, self.STATUS_OK)
        self.assertContains(response, "test expense")
        self.assertNotContains(response, "other user expense")
