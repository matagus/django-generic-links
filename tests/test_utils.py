from django.contrib.auth.models import User
from django.test import TestCase

from generic_links.models import GenericLink
from generic_links.utils import get_links_for
from tests.models import TaggedItem


class GetLinksForTest(TestCase):
    def setUp(self):
        self.item = TaggedItem.objects.create(name="item")
        self.other_item = TaggedItem.objects.create(name="other")

        self.external = GenericLink.objects.create(
            title="External",
            url="https://external.example.com",
            content_object=self.item,
            is_external=True,
        )
        self.internal = GenericLink.objects.create(
            title="Internal",
            url="https://internal.example.com",
            content_object=self.item,
            is_external=False,
        )
        self.other_link = GenericLink.objects.create(
            title="Other",
            url="https://other.example.com",
            content_object=self.other_item,
        )

    def test_all_links_for_object(self):
        links = get_links_for(self.item)
        self.assertCountEqual([link.pk for link in links], [self.external.pk, self.internal.pk])

    def test_external_only(self):
        links = get_links_for(self.item, is_external=True)
        self.assertEqual([link.pk for link in links], [self.external.pk])

    def test_internal_only(self):
        links = get_links_for(self.item, is_external=False)
        self.assertEqual([link.pk for link in links], [self.internal.pk])

    def test_selects_related_user(self):
        creator = User.objects.create_user(username="creator", password="pw")
        self.external.user = creator
        self.external.save()

        with self.assertNumQueries(1):
            link = get_links_for(self.item).get(pk=self.external.pk)
            self.assertEqual(link.user, creator)
