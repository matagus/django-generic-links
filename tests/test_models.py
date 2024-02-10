from __future__ import annotations

from django.contrib.auth.models import User
from django.test import TestCase

from generic_links.models import GenericLink


class ModelTest(TestCase):
    def test_str(self):
        user = User.objects.create(username="Test User")

        link = GenericLink.objects.create(
            title="Test Title",
            url="https://www.test.com",
            description="Test Description",
            content_object=user,
        )

        self.assertEqual(str(link), f"{link.title} :: {link.url}")
