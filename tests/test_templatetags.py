from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.template import Context
from django.template import Template
from django.test import TestCase

from generic_links.models import GenericLink


class TemplateTagTestCase(TestCase):
    """
    Test case for the template tag  `get_links_for <obj>` in the `generic_links_tags.py` file.
    """

    def setUp(self):
        content_type = ContentType.objects.get_for_model(User)

        self.user1 = User.objects.create(username="test_user")

        self.link1 = GenericLink.objects.create(
            url="https://example.com/path/to/this-thing/",
            content_type=content_type,
            object_id=self.user1.id,
        )

        self.link2 = GenericLink.objects.create(
            url="https://example.com/path/to/other-thing/",
            content_type=content_type,
            object_id=self.user1.id,
        )

        self.user2 = User.objects.create(username="test_user2")

        self.link3 = GenericLink.objects.create(
            url="https://example.com/foobar/",
            content_type=content_type,
            object_id=self.user2.id,
        )

    def test_get_links_for(self):
        """
        Test the `get_links_for` template tag.
        """

        template_string = """
            {% load generic_links_tags %}
            {% get_links_for my_obj as links_qs %}
            {% for link in links_qs %}
                {{ link.url }}
            {% endfor %}
        """

        template = Template(template_string)

        rendered_string = template.render(Context({"my_obj": self.user1}))

        self.assertIn(self.link1.url, rendered_string)
        self.assertIn(self.link2.url, rendered_string)
        self.assertNotIn(self.link3.url, rendered_string)

        rendered_string2 = template.render(Context({"my_obj": self.user2}))

        self.assertEqual(self.link3.url, rendered_string2.strip())
