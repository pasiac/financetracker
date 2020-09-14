from django.test import TestCase

from accounts.factories import UserFactory
from categories.factories import CategoryFactory
from categories.models import Category
from utils.tests.mixins import TestUtilityMixin


class TestEdit(TestCase, TestUtilityMixin):
    def setUp(self):
        self.user = UserFactory.create()
        self.category = CategoryFactory.create(created_by=self.user)
        self.url = f"/kategorie/edytuj/{self.category.id}/"

    def test_user_cant_enter_edit_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertNotEqual(response.status_code, self.STATUS_OK)

    def test_user_can_see_edit_form_after_log_in(self):
        self.__given_user_logged_in()
        response = self.client.get(self.url)
        self.assertContains(response, "Edycja kategorii")

    def test_user_redirected_after_success_edit(self):
        self.__given_user_logged_in()
        response = self.client.post(self.url, {"title": "new title"})
        self.__then_category_title_and_value_changed()
        self.__then_redirected_to_category_list(response)

    def test_user_get_404_when_edit_non_existing_category(self):
        self.__given_user_logged_in()
        non_existing_category_id = self.category.id + 1
        url = f"wydatki/edytuj/{non_existing_category_id}"
        response = self.client.post(url, {"title": "new title"})
        self.assertEqual(response.status_code, self.STATUS_NOT_FOUND)

    def __given_user_logged_in(self):
        self.client.force_login(self.user, backend=None)

    def __then_category_title_and_value_changed(self):
        category = Category.objects.get(pk=self.category.id)
        self.assertEqual(category.title, "new title")

    def __then_redirected_to_category_list(self, response):
        self.was_redirected_to("/kategorie/", response)
