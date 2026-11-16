from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator
from django.db import models
from django.test import TestCase

from generic_links.models import DESCRIPTION_MAX_LENGTH, GenericLink
from generic_links.utils import get_links_for
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


class ObjectIdFieldTest(TestCase):
    """
    ``object_id`` has to be wide enough to hold the primary keys of the models it
    points at. ``DEFAULT_AUTO_FIELD`` is ``BigAutoField`` (64-bit), so a 32-bit
    column overflows: SQLite stores the value silently while PostgreSQL rejects
    the INSERT with "integer out of range".
    """

    # Beyond the 32-bit signed maximum, i.e. unreachable for a PositiveIntegerField.
    BIG_PK = 2**32

    def test_object_id_is_a_big_integer_field(self):
        field = GenericLink._meta.get_field("object_id")
        self.assertIsInstance(field, models.PositiveBigIntegerField)

    def test_object_id_round_trips_a_value_beyond_int32(self):
        link = GenericLink.objects.create(
            title="Big",
            url="https://big.example.com",
            content_type_id=1,
            object_id=self.BIG_PK,
        )

        link.refresh_from_db()

        self.assertEqual(link.object_id, self.BIG_PK)

    def test_links_to_a_content_object_with_a_big_pk_are_retrievable(self):
        item = TaggedItem.objects.create(name="big", pk=self.BIG_PK)
        link = GenericLink.objects.create(
            title="Doc",
            url="https://docs.example.com",
            content_object=item,
        )

        self.assertEqual(link.object_id, self.BIG_PK)
        self.assertEqual(list(get_links_for(item)), [link])


class DescriptionMaxLengthTest(TestCase):
    """
    ``description`` declares ``max_length`` on a ``TextField``. Unlike
    ``CharField``, a ``TextField`` does not install a ``MaxLengthValidator`` on
    the model, so the limit has to be declared explicitly or model-level
    validation silently accepts anything.
    """

    def setUp(self):
        self.item = TaggedItem.objects.create(name="item")

    def build(self, description: str) -> GenericLink:
        return GenericLink(
            title="Doc",
            url="https://docs.example.com",
            description=description,
            content_object=self.item,
        )

    def test_full_clean_accepts_a_description_at_the_limit(self):
        link = self.build("x" * DESCRIPTION_MAX_LENGTH)

        link.full_clean()  # must not raise

    def test_full_clean_rejects_a_description_over_the_limit(self):
        link = self.build("x" * (DESCRIPTION_MAX_LENGTH + 1))

        with self.assertRaises(ValidationError) as ctx:
            link.full_clean()

        self.assertIn("description", ctx.exception.message_dict)

    def test_model_field_declares_a_max_length_validator(self):
        field = GenericLink._meta.get_field("description")

        self.assertTrue(
            any(isinstance(v, MaxLengthValidator) for v in field.validators),
            f"expected a MaxLengthValidator on description, got {field.validators}",
        )
