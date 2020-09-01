from django.shortcuts import reverse
from django.test import RequestFactory, TestCase

from tracker.factories import ExpenseFactory, UserFactory
from tracker.models import Expense
from tracker.views import delete_expanse, expanse_detail, expense_list

STATUS_OK = 200
STATUS_REDIRECTED = 302 or 301


class TestIndex(TestCase):
    def test_index(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, STATUS_OK)


class TestExploreexpense(TestCase):
    def setUp(self):
        self.request = RequestFactory()
        self.user = UserFactory()

    def test_return_single_user_expanse(self):
        Expense = ExpenseFactory(user=self.user)
        request = self.request.get(reverse("expense_list"))
        request.user = self.user
        response = expense_list(request)
        self.assertContains(response, Expense.value)

    def test_return_list_of_user_expense(self):
        self.__create_list_of_expense_for_user()
        request = self.request.get(reverse("expense_list"))
        request.user = self.user
        response = expense_list(request)
        self.__assert_list_of_expense(response)

    def test_delete_income_outcome(self):
        Expense = ExpenseFactory(user=self.user)
        object_to_delete_id = Expense.id
        request = self.request.get(reverse("expense_list"))
        request.user = self.user
        response = delete_expanse(request, object_to_delete_id)
        Expense = Expense.objects.filter(id=object_to_delete_id).first()
        self.assertIsNone(Expense)
        self.assertEqual(response.status_code, STATUS_REDIRECTED)

    def test_get_expanse_details(self):
        Expense = ExpenseFactory(user=self.user)
        request = self.request.get(
            reverse("expanse_detail", kwargs={"expanse_id": Expense.id})
        )
        request.user = self.user
        response = expanse_detail(request, Expense.id)
        self.__assert_all_fields_of_details(response, Expense)

    # def test_add_expanse_should_add_new_expanse_if_correct_data(self):
    #     data = {
    #         "title": "test",
    #         "value": "100",
    #         "category": CategoryFactory(user=self.user),
    #     }
    #     request = self.request.get(reverse("add_expanse"))
    #     request.user = self.user
    #     response = add_expanse(request)
    #     counted_objects = Expense.objects.count()
    #     # self.assertEqual(1, counted_objects)
    #     # ??????

    def __create_list_of_expense_for_user(self):
        return [
            ExpenseFactory(user=self.user, title=f"test{x}") for x in range(10)
        ]

    def __assert_list_of_expense(self, response):
        for x in range(10):
            self.assertContains(response, f"test{x}")

    def __assert_all_fields_of_details(self, response, Expense: Expense):
        self.assertContains(response, Expense.title)
        self.assertContains(response, Expense.value)
        self.assertContains(response, Expense.category)
