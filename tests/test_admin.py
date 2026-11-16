from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db import connection
from django.test import TestCase
from django.test.utils import CaptureQueriesContext
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

    def test_list_select_related_covers_the_user_column(self):
        # "user" is in list_display, so it must be joined eagerly. Django's
        # default is False and True means "join every FK", so accept either a
        # truthy True or a sequence naming user -- but fail cleanly on False
        # rather than raising TypeError from the membership test.
        value = GenericLinkAdmin.list_select_related
        covers_user = value is True or (isinstance(value, (list, tuple)) and "user" in value)
        self.assertTrue(covers_user, f'expected list_select_related to cover "user", got {value!r}')


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

    def test_changelist_query_count_does_not_grow_with_the_number_of_rows(self):
        """
        ``list_display`` shows ``user``. Without ``list_select_related`` the
        changelist issues one extra query per row to fetch it (measured: 6
        queries for 5 rows instead of 1).

        Comparing two page sizes rather than pinning an absolute count keeps the
        test independent of how many queries the admin needs for sessions,
        permissions and filters, which varies between Django versions.
        """
        item = TaggedItem.objects.create(name="item")

        def changelist_queries(batch: str, rows: int) -> int:
            for i in range(rows):
                GenericLink.objects.create(
                    title=f"Link {batch}-{i}",
                    url=f"https://example.com/{batch}/{i}/",
                    content_object=item,
                    user=User.objects.create_user(username=f"creator-{batch}-{i}"),
                )
            with CaptureQueriesContext(connection) as ctx:
                response = self.client.get(self.changelist_url)
            self.assertEqual(response.status_code, 200)
            return len(ctx.captured_queries)

        # Both batches stay well under the default list_per_page of 100, so each
        # request renders a single page.
        small = changelist_queries("small", 2)
        large = changelist_queries("large", 20)

        self.assertEqual(
            small,
            large,
            f"changelist issued {small} queries for 2 rows but {large} for 22; "
            "the per-row count grew, so user is not being select_related'd",
        )
