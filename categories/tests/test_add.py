from django.test import TestCase

from accounts.factories import UserFactory
from categories.factories import CategoryFactory
from categories.models import Category
from utils.tests.mixins import TestUtilityMixin


class TestViewCategoryAdd(TestCase, TestUtilityMixin):
    url = "/kategorie/dodaj/"

    def setUp(self):
        self.user = UserFactory.create()
        self.existing_category = CategoryFactory.create(created_by=self.user)
        self.new_category_data = {
            "title": "New test category",
        }

    def test_not_loged_in_user_cant_add(self):
        response = self.client.post(self.url, self.new_category_data)
        self.assertNotEqual(response.status_code, self.STATUS_OK)

    def test_get_category_form(self):
        self.client.force_login(self.user, backend=None)

        url = self.url.format(self.existing_category.id)
        response = self.client_send_request_with_params(url, self.new_category_data)
        self.assertEqual(response.status_code, self.STATUS_OK)

    def test_add_category_when_missing_required_data_fails(self):
        self.client.force_login(self.user, backend=None)

        response = self.client_send_post_request(self.url, {})
        self.assertFalse(response.context["form"].is_valid())

    def test_add_category_ok(self):
        self.client.force_login(self.user, backend=None)

        response = self.client.post(self.url, self.new_category_data)
        created_category = Category.objects.get(pk=self.existing_category.pk + 1)
        expected_location = "/kategorie/"
        self.assertTrue(self.was_redirected_to(expected_location, response))
        self.assertEqual(created_category.title, self.new_category_data["title"])
