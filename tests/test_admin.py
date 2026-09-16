from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from django.urls import reverse

from generic_links.admin import GenericLinkAdmin, GenericLinkStackedInline, GenericLinkTabularInline
from generic_links.models import GenericLink
from tests.models import TaggedItem


class AdminRegistrationTest(TestCase):
    def test_generic_link_registered(self):
        self.assertIn(GenericLink, admin.site._registry)
        self.assertIsInstance(admin.site._registry[GenericLink], GenericLinkAdmin)

    def test_inline_classes(self):
        for inline_class in (GenericLinkStackedInline, GenericLinkTabularInline):
            self.assertIs(inline_class.model, GenericLink)
            self.assertEqual(inline_class.extra, 1)


class AdminViewsTest(TestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(username="admin", email="admin@example.com", password="pw")
        self.client.force_login(self.superuser)
        self.changelist_url = reverse("admin:generic_links_genericlink_changelist")

    def test_changelist_renders_links(self):
        item = TaggedItem.objects.create(name="item")
        GenericLink.objects.create(
            title="Doc link",
            url="https://docs.example.com",
            description="A description",
            content_object=item,
            user=self.superuser,
        )

        response = self.client.get(self.changelist_url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Doc link")
        self.assertContains(response, "https://docs.example.com")

    def test_add_link_via_admin(self):
        item = TaggedItem.objects.create(name="item")
        data = {
            "content_type": ContentType.objects.get_for_model(TaggedItem).pk,
            "object_id": item.pk,
            "url": "https://example.com",
            "title": "Example",
            "description": "",
            "user": "",
            "is_external": "on",
        }

        response = self.client.post(reverse("admin:generic_links_genericlink_add"), data, follow=True)

        self.assertEqual(response.status_code, 200)
        link = GenericLink.objects.get(title="Example")
        self.assertEqual(link.content_object, item)
        self.assertTrue(link.is_external)
