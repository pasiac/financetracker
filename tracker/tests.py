from django.shortcuts import reverse
from django.test import TestCase, RequestFactory
from .views import explore_expanses
from .factories import UserFactory, IncomeOutcomeFactory
from django.contrib.auth.models import AnonymousUser

STATUS_OK = 200


class TestIndex(TestCase):
    def test_index(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, STATUS_OK)


class TestExploreExpanses(TestCase):
    def setUp(self):
        self.request = RequestFactory()
        self.user = UserFactory()


    def test_return_prompt_to_login_if_user_isnt_log_in(self):
        request = self.request.get(reverse("expanses"))
        request.user = AnonymousUser()
        response = explore_expanses(request)
        self.assertContains(response, "Zaloguj sie, zeby przegladac swoje wydatki")

    def test_return_single_user_expanse(self):
        incomeOutcome = IncomeOutcomeFactory(user=self.user)
        request = self.request.get(reverse("expanses"))
        request.user = self.user
        response = explore_expanses(request)
        self.assertContains(response, incomeOutcome.value)

    def test_return_list_of_user_expanses(self):
        income_outcomes =self.__create_list_of_expanses_for_user()
        print(income_outcomes)
        request = self.request.get(reverse("expanses"))
        request.user = self.user
        response = explore_expanses(request)
        self.__assert_list_of_expanses
    

    def __create_list_of_expanses_for_user(self):
        return [IncomeOutcomeFactory(user=self.user, title=f"test{x}") for x in range(10)]

    def __assert_list_of_expanses(self, response):
        for x in range(10):
            self.assertContains(response, f"test{x}")
        
