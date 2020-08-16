from unittest.mock import patch

from django.contrib.auth.models import AnonymousUser
from django.shortcuts import reverse
from django.test import RequestFactory, TestCase

from .factories import CategoryFactory, IncomeOutcomeFactory, UserFactory
from .models import IncomeOutcome
from .views import add_expanse, delete_expanse, expanse_detail, expanses_list

STATUS_OK = 200
STATUS_REDIRECTED = 302 or 301


class TestIndex(TestCase):
    def test_index(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, STATUS_OK)


class TestExploreExpanses(TestCase):
    def setUp(self):
        self.request = RequestFactory()
        self.user = UserFactory()

    def test_return_single_user_expanse(self):
        incomeOutcome = IncomeOutcomeFactory(user=self.user)
        request = self.request.get(reverse("expanses_list"))
        request.user = self.user
        response = expanses_list(request)
        self.assertContains(response, incomeOutcome.value)

    def test_return_list_of_user_expanses(self):
        income_outcomes = self.__create_list_of_expanses_for_user()
        request = self.request.get(reverse("expanses_list"))
        request.user = self.user
        response = expanses_list(request)
        self.__assert_list_of_expanses(response)

    def test_delete_income_outcome(self):
        incomeOutcome = IncomeOutcomeFactory(user=self.user)
        object_to_delete_id = incomeOutcome.id
        request = self.request.get(reverse("expanses_list"))
        request.user = self.user
        response = delete_expanse(request, object_to_delete_id)
        incomeOutcome = IncomeOutcome.objects.filter(id=object_to_delete_id).first()
        self.assertIsNone(incomeOutcome)
        self.assertEqual(response.status_code, STATUS_REDIRECTED)

    def test_get_expanse_details(self):
        incomeOutcome = IncomeOutcomeFactory(user=self.user)
        request = self.request.get(
            reverse("expanse_detail", kwargs={"expanse_id": incomeOutcome.id})
        )
        request.user = self.user
        response = expanse_detail(request, incomeOutcome.id)
        self.__assert_all_fields_of_details(response, incomeOutcome)

    def test_add_expanse_should_add_new_expanse_if_correct_data(self):
        data = {
            "title": "test",
            "value": "100",
            "category": CategoryFactory(user=self.user),
        }
        request = self.request.get(reverse("add_expanse"))
        request.user = self.user
        response = add_expanse(request)
        counted_objects = IncomeOutcome.objects.count()
        # self.assertEqual(1, counted_objects)
        # ??????

    def __create_list_of_expanses_for_user(self):
        return [
            IncomeOutcomeFactory(user=self.user, title=f"test{x}") for x in range(10)
        ]

    def __assert_list_of_expanses(self, response):
        for x in range(10):
            self.assertContains(response, f"test{x}")

    def __assert_all_fields_of_details(self, response, incomeOutcome: IncomeOutcome):
        self.assertContains(response, incomeOutcome.title)
        self.assertContains(response, incomeOutcome.value)
        self.assertContains(response, incomeOutcome.category)
