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
