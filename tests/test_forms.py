from django.test import TestCase

from generic_links.forms import AddLinkForm


class AddFormTest(TestCase):
    def setUp(self):
        self.initial_kwargs = dict(user=None, object_id="1", content_type="1")

    def test_add_form_without_data(self):
        form = AddLinkForm(**self.initial_kwargs)
        self.assertFalse(form.is_valid())

    def test_add_form_with_incomplete_data(self):
        form = AddLinkForm(data={"url": "http://www.example.com"}, **self.initial_kwargs)
        self.assertFalse(form.is_valid())

    def test_add_form_with_complete_data(self):
        form = AddLinkForm(data={"url": "http://www.example.com", "title": "Example"}, **self.initial_kwargs)
        self.assertTrue(form.is_valid())
