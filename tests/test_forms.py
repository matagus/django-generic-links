from django.contrib.auth.models import User
from django.test import TestCase

from generic_links.forms import AddLinkForm


class AddFormTest(TestCase):
    def setUp(self):
        self.content_object = User.objects.create_user(username="test", password="test")
        self.initial_args = (self.content_object, None)

    def test_add_form_without_data(self):
        form = AddLinkForm(*self.initial_args)
        self.assertFalse(form.is_valid())

    def test_add_form_with_incomplete_data(self):
        form = AddLinkForm(*self.initial_args, data={"url": "http://www.example.com"})
        self.assertFalse(form.is_valid())

    def test_add_form_with_complete_data(self):
        form = AddLinkForm(*self.initial_args, data={"url": "http://www.example.com", "title": "Example"})
        self.assertTrue(form.is_valid())

        new_link = form.save()
        self.assertEqual(new_link.url, "http://www.example.com")
        self.assertEqual(new_link.title, "Example")
        self.assertEqual(new_link.user, None)
        self.assertEqual(new_link.content_object, self.content_object)
        self.assertEqual(new_link.is_external, False)
