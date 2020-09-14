from django.test import TestCase

from accounts.factories import UserFactory
from categories.factories import CategoryFactory
from categories.models import Category
from utils.tests.mixins import TestUtilityMixin


class TestDelete(TestCase, TestUtilityMixin):
    def setUp(self):
        self.user = UserFactory.create()
        self.category = CategoryFactory.create(created_by=self.user)
        self.url = f"/kategorie/usun/{self.category.id}/"

    def test_user_cant_delete_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertNotEqual(response.status_code, self.STATUS_OK)

    def test_user_can_delete_after_log_in(self):
        self.__given_user_logged_in()
        before = Category.objects.count()
        response = self.client.post(self.url)
        after = Category.objects.count()
        self.assertEqual(before, after + 1)
        self.__then_redirected_to_category_list(response)

    def test_user_get_404_when_delete_non_existing_category(self):
        self.__given_user_logged_in()
        non_existing_category_id = self.category.id + 1
        url = f"kategorie/usun/{non_existing_category_id}"
        response = self.client.post(url)
        self.assertEqual(response.status_code, self.STATUS_NOT_FOUND)

    def __given_user_logged_in(self):
        self.client.force_login(self.user, backend=None)

    def __then_redirected_to_category_list(self, response):
        self.was_redirected_to("/wydatki/", response)
