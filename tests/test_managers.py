from django.contrib.auth.models import User
from django.test import TestCase

from generic_links.models import GenericLink


class ModelTest(TestCase):
    def test_external_and_internal(self):
        user = User.objects.create(username="Test User")

        external_link = GenericLink.objects.create(
            title="An external link",
            url="https://www.test.com",
            description="An external link for this user",
            content_object=user,
            is_external=True,
        )

        internal_link = GenericLink.objects.create(
            title="An internal link",
            url="https://www.test.com",
            description="An internal link for this user",
            content_object=user,
            is_external=False,
        )

        self.assertEqual(GenericLink.objects.count(), 2)

        external_qs = GenericLink.objects.external()

        self.assertEqual(external_qs.count(), 1)
        self.assertListEqual([link.id for link in external_qs], [external_link.id])

        internal_qs = GenericLink.objects.internal()

        self.assertEqual(internal_qs.count(), 1)
        self.assertListEqual([link.id for link in internal_qs], [internal_link.id])

    def test_by_user(self):
        user1 = User.objects.create(username="user1")

        link = GenericLink.objects.create(
            title="Test Title",
            url="https://www.test.com",
            description="Test Description",
            content_object=user1,
            user=user1,
        )

        user2 = User.objects.create(username="user2")

        link2 = GenericLink.objects.create(
            title="Second Test Title",
            url="https://www.test.com",
            description="Test Description for user 2",
            content_object=user2,
            user=user1,
        )

        self.assertEqual(GenericLink.objects.count(), 2)

        self.assertEqual(GenericLink.objects.by_user(user1).count(), 2)
        self.assertSetEqual({link.id for link in GenericLink.objects.by_user(user1)}, {link.id, link2.id})

        self.assertEqual(GenericLink.objects.by_user(user2).count(), 0)
