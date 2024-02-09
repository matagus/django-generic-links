from __future__ import annotations

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from generic_links.models import GenericLink


class ModelTest(TestCase):
    def test_str(self):
        user = User.objects.create(username="Test User")
        content_type = ContentType.objects.get_for_model(User)

        link = GenericLink.objects.create(
            title="Test Title",
            url="https://www.test.com",
            description="Test Description",
            content_type=content_type,
            object_id=user.id,
        )

        self.assertEqual(str(link), f"{link.title} :: {link.url}")
