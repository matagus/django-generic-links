from django.contrib.auth.models import User
from django.test import TestCase

from generic_links.forms import AddLinkForm
from generic_links.models import GenericLink


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
        # Unchecked checkboxes are absent from POST data, so is_external is False
        self.assertEqual(new_link.is_external, False)

    def test_unbound_form_initial_is_external_true(self):
        form = AddLinkForm(*self.initial_args)
        self.assertTrue(form.fields["is_external"].initial)

    def test_add_form_with_is_external_checked(self):
        form = AddLinkForm(
            *self.initial_args,
            data={"url": "http://www.example.com", "title": "Example", "is_external": "on"},
        )
        self.assertTrue(form.is_valid())

        new_link = form.save()
        self.assertTrue(new_link.is_external)

    def test_add_form_with_user(self):
        creator = User.objects.create_user(username="creator", password="pw")
        form = AddLinkForm(
            self.content_object,
            creator,
            data={"url": "http://www.example.com", "title": "Example"},
        )
        self.assertTrue(form.is_valid())

        new_link = form.save()
        self.assertEqual(new_link.user, creator)

    def test_save_with_commit_false(self):
        form = AddLinkForm(*self.initial_args, data={"url": "http://www.example.com", "title": "Example"})
        self.assertTrue(form.is_valid())

        new_link = form.save(commit=False)

        self.assertIsNone(new_link.pk)
        self.assertEqual(GenericLink.objects.count(), 0)

        new_link.save()
        self.assertEqual(GenericLink.objects.count(), 1)
        self.assertEqual(new_link.content_object, self.content_object)

    def test_add_form_saves_description(self):
        form = AddLinkForm(
            *self.initial_args,
            data={
                "url": "http://www.example.com",
                "title": "Example",
                "description": "An example description",
            },
        )
        self.assertTrue(form.is_valid())

        new_link = form.save()
        self.assertEqual(new_link.description, "An example description")

        new_link.refresh_from_db()
        self.assertEqual(new_link.description, "An example description")
