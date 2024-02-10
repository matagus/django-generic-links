from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from generic_links.forms import AddLinkForm


class AddFormTest(TestCase):
    def setUp(self):
        content_type = ContentType.objects.get_for_model(User)
        self.initial_kwargs = dict(user=None, object_id=1, content_type=content_type)

    def test_add_form_without_data(self):
        form = AddLinkForm(**self.initial_kwargs)
        self.assertFalse(form.is_valid())

    def test_add_form_with_incomplete_data(self):
        form = AddLinkForm(data={"url": "http://www.example.com"}, **self.initial_kwargs)
        self.assertFalse(form.is_valid())

    def test_add_form_with_complete_data(self):
        form = AddLinkForm(data={"url": "http://www.example.com", "title": "Example"}, **self.initial_kwargs)
        self.assertTrue(form.is_valid())

        new_link = form.save()
        print(new_link.content_object)
        self.assertEqual(new_link.url, "http://www.example.com")
        self.assertEqual(new_link.title, "Example")
        self.assertEqual(new_link.user, None)
        self.assertEqual(new_link.object_id, 1)
        self.assertEqual(new_link.content_type_id, self.initial_kwargs["content_type"].id)
        self.assertEqual(new_link.is_external, False)
