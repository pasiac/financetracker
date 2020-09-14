from django.test import TestCase

from accounts.factories import UserFactory
from categories.factories import CategoryFactory
from utils.tests.mixins import TestUtilityMixin


class TestList(TestCase, TestUtilityMixin):
    url = "/kategorie/"

    def setUp(self):
        self.user = UserFactory.create()
        self.category_per_page = 10
        self.paging_element = "paging_grip"

    def test_user_cant_see_category_list_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertNotEqual(response.status_code, self.STATUS_OK)

    def test_user_can_see_his_categories_after_log_in(self):
        self.__given_user_logged_in()
        self.__given_categories_created()
        response = self.client.get(self.url)
        self.__then_logged_in_user_categories_shown(response)

    def test_returns_ok_when_there_are_multiple_page_of_categories(
        self,
    ):
        self.__given_user_logged_in()
        CategoryFactory.create_batch(
            size=self.category_per_page + 1, created_by=self.user
        )

        response = self.client.get(self.url)
        self.assertEqual(self.STATUS_OK, response.status_code)
        self.assertContains(response, "&laquo;")

    def __given_user_logged_in(self):
        self.client.force_login(self.user, backend=None)

    def __given_categories_created(self):
        CategoryFactory.create(title="test category", created_by=self.user)
        CategoryFactory.create(title="other user category")

    def __then_logged_in_user_categories_shown(self, response):
        self.assertEqual(response.status_code, self.STATUS_OK)
        self.assertContains(response, "test category")
        self.assertNotContains(response, "other user category")
