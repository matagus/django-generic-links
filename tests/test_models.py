from django.contrib.auth.models import User
from django.test import TestCase

from generic_links.models import GenericLink
from tests.models import TaggedItem


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


class GenericRelationTest(TestCase):
    def test_tagged_item_str(self):
        item = TaggedItem.objects.create(name="item")
        self.assertEqual(str(item), "item")

    def test_reverse_generic_relation(self):
        item = TaggedItem.objects.create(name="item")
        link = GenericLink.objects.create(title="Doc", url="https://docs.example.com", content_object=item)

        self.assertEqual(list(item.generic_links.all()), [link])

    def test_deleting_content_object_cascades_via_generic_relation(self):
        item = TaggedItem.objects.create(name="item")
        GenericLink.objects.create(title="Doc", url="https://docs.example.com", content_object=item)
        self.assertEqual(GenericLink.objects.count(), 1)

        item.delete()

        self.assertEqual(GenericLink.objects.count(), 0)
